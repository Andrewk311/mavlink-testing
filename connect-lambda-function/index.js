const AWS = require('aws-sdk');
const dynamoDB = new AWS.DynamoDB.DocumentClient();

const tableName = 'WebSocketConnections';

exports.handler = async (event) => {
  console.log("Connect Lambda: Event:", JSON.stringify(event, null, 2));

  const connectionId = event.requestContext.connectionId;
  console.log("Correct connection lambda");
  
  // Save connectionId to the DynamoDB table
  const putParams = {
    TableName: tableName,
    Item: {
      connectionId: connectionId,
    },
  };

  try {
    await dynamoDB.put(putParams).promise();
  } catch (error) {
    console.error('Error saving connectionId:', error);
    return {
      statusCode: 500,
      body: 'Failed to connect: ' + JSON.stringify(error),
    };
  }

  return {
    statusCode: 200,
    body: 'Connected',
  };
};
