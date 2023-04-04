// disconnect.js
const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

const deleteConnection = async (connectionId) => {
  const params = {
    TableName: "WebSocketConnections",
    Key: {
      connectionId,
    },
  };

  await dynamoDb.delete(params).promise();
};

exports.handler = async (event) => {
  const connectionId = event.requestContext.connectionId;
  await deleteConnection(connectionId);

  return {
    statusCode: 200,
    body: 'Disconnected',
  };
};
