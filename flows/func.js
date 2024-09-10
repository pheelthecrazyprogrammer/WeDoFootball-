// This file demonstrates the use of JavaScript in our project.
// It is created to illustrate the broad usage of JavaScript in handling various tasks.

// Retrieve the topic from the flow context
var player_topic = flow.get('player_topic');

// Check if the message topic matches the retrieved topic
if (msg.topic === player_topic) {
    // Extract systolic and diastolic blood pressure values from the message payload
    var systolic = msg.payload.blood_pressure.systolic;
    var diastolic = msg.payload.blood_pressure.diastolic;

    // Round systolic and diastolic values to the nearest integer
    var roundedSystolic = Math.round(systolic);
    var roundedDiastolic = Math.round(diastolic);

    // Create a new object with rounded blood pressure values
    msg.payload = {
        blood_pressure: {
            systolic: roundedSystolic,
            diastolic: roundedDiastolic
        }
    };

    // Return the modified message
    return msg;
} else {
    // Return null if the message topic does not match
    return null;
}
