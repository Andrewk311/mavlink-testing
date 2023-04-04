const AWS = require('aws-sdk');
const apiGatewayManagementApi = new AWS.ApiGatewayManagementApi();

exports.handler = async (event) => {
  console.log('Received event:', JSON.stringify(event, null, 2));

  const { body, requestContext } = event;
  const { connectionId, domainName, stage } = requestContext;

  const parsedBody = JSON.parse(body);
  const { type } = parsedBody;

  if (type === 'ping') {
    // Respond with 'pong' message
    await sendPongMessage(connectionId, domainName, stage);
  }

  return { statusCode: 200 };
};

async function sendPongMessage(connectionId, domainName, stage) {
  const params = {
    ConnectionId: connectionId,
    Data: JSON.stringify({ type: 'pong' }),
  };

  apiGatewayManagementApi.endpoint = new AWS.Endpoint(`https://${domainName}/${stage}`);
  return apiGatewayManagementApi.postToConnection(params).promise();
}
