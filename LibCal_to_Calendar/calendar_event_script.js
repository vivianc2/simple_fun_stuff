function createEventFromRecentEmails() {
    var calendarId = 'CALENDAR_ID';

    // Get the current date and time
    var now = new Date();

    // Calculate the time one hour ago
    var oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
    Logger.log('Processing emails received after: ' + oneHourAgo);

    // Calculate the time 7 days ago
    var sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    var formattedSevenDaysAgo = Utilities.formatDate(sevenDaysAgo, Session.getScriptTimeZone(), 'yyyy/MM/dd');

    // Search for emails with the specific subject received in the last 7 days
    var searchQuery = 'subject:"Your booking has been submitted" after:' + formattedSevenDaysAgo;
    var threads = GmailApp.search(searchQuery);

    if (threads.length == 0) {
        Logger.log("No threads found with the specified subject in the past 7 days.");
        return;
    }

    // Loop through all threads (emails)
    for (var i = 0; i < threads.length; i++) {
        var messages = threads[i].getMessages();

        // Loop through all messages in the thread
        for (var j = 0; j < messages.length; j++) {
            var message = messages[j];

            // Check if the message was received within the last hour
            var messageDate = message.getDate();
            Logger.log('Message received at: ' + messageDate);

            if (messageDate < oneHourAgo) {
                Logger.log('Message is older than one hour, skipping.');
                continue;
            }

            var plainBody = message.getPlainBody(); // Extract the plain text version of the email

            // Remove HTML tags from the plain text and add line breaks
            var cleanedBody = plainBody.replace(/<br\s*\/?>/g, '\n')
                .replace(/<[^>]+>/g, '')
                .trim();
            Logger.log(cleanedBody);

            // Split the cleaned body into lines
            var lines = cleanedBody.split('\n');

            lines.forEach(function (line) {
                // Match lines that contain room and time information
                var eventRegex = /^(.+?):\s*(\d{1,2}:\d{2}[ap]m) - (\d{1,2}:\d{2}[ap]m), (.+)$/;
                var match = line.match(eventRegex);

                if (match) {
                    var room = match[1];  // Extract the room or location name
                    var startTimeString = match[2];  // Extract the start time
                    var endTimeString = match[3];  // Extract the end time
                    var dateString = match[4];  // Extract the date

                    Logger.log('Room: ' + room);
                    Logger.log('Start Time String: ' + startTimeString);
                    Logger.log('End Time String: ' + endTimeString);
                    Logger.log('Date String: ' + dateString);

                    var startTime = new Date(dateString + ' ' + startTimeString.replace(/am/, ' AM').replace(/pm/, ' PM'));
                    var endTime = new Date(dateString + ' ' + endTimeString.replace(/am/, ' AM').replace(/pm/, ' PM'));

                    Logger.log('Parsed Start Time: ' + startTime);
                    Logger.log('Parsed End Time: ' + endTime);

                    if (isNaN(startTime.getTime()) || isNaN(endTime.getTime())) {
                        Logger.log('Invalid start or end time. Skipping this event.');
                        return;
                    }

                    var title = room;// + ': ' + startTimeString + ' - ' + endTimeString;

                    var calendar = CalendarApp.getCalendarById(calendarId);
                    calendar.createEvent(title, startTime, endTime, {
                        location: room,
                        description: 'Reserved via LibCal'
                    });

                    Logger.log('Event created: ' + title);
                }
            });
        }
    }
}
