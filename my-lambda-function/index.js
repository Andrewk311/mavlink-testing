const AWS = require("aws-sdk");
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const apiGatewayManagementApi = new AWS.ApiGatewayManagementApi({
  apiVersion: "2018-11-29",
  endpoint: "07k3svmpdh.execute-api.us-east-1.amazonaws.com/production",
});

const deleteConnection = async (connectionId) => {
  const params = {
    TableName: "WebSocketConnections",
    Key: {
      connectionId,
    },
  };

  await dynamoDb.delete(params).promise();
};

const getAllConnections = async () => {
  const params = {
    TableName: "WebSocketConnections",
  };

  const result = await dynamoDb.scan(params).promise();
  return result.Items;
};

const sendToClient = async (connectionId, data) => {
  try {
    await apiGatewayManagementApi
      .postToConnection({ ConnectionId: connectionId, Data: data })
      .promise();
  } catch (error) {
    console.error("Error sending message to client:", error);
    if (error.statusCode === 410) {
      // GoneException indicates that the connection no longer exists.
      // Remove it from the database.
      await deleteConnection(connectionId);
    }
  }
};

exports.handler = async (event) => {
  const action = event.requestContext.routeKey;
  const data = JSON.parse(event.body);
  const connectionId = event.requestContext.connectionId;

  if (action === "$disconnect") {
    await deleteConnection(connectionId);
  } else {
    // Broadcast the received message to all connected clients
    const connections = await getAllConnections();

    await Promise.all(
      connections.map(({ connectionId }) =>
        sendToClient(connectionId, JSON.stringify(data))
      )
    );
  }

  return {
    statusCode: 200,
    headers: {
      "Access-Control-Allow-Origin": "https://pharmacy.valkyriedrone.io/orders/",
      "Access-Control-Allow-Credentials": true,
    },
    body: "Message processed",
  };
};
