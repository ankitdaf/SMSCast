SMSCast
============

SMSCast is a group messaging solution using txtweb + Google App Engine.

What it can do
--------------
SMSCast will read messages sent by anyone from a registered userbase and re-broadcast it to that userbase

Use Case
--------
SMSCast is pretty useful for small groups that can be used to quickly convey information.

Additional Information
----------------------
There is an inbuilt check to ensure that messages come from txtweb and mobile phone numbers, and are not exploited on the web by spammers

Limitations
-----------
txtweb imposes a 5000 PUSH text messages per day limit. This means the app will be able to send 5000 messages **in all** to the group, **not individually**

TODO
----

- Impose a 5-messages per hour limit for each user to avoid unnecessary spamming
- Add a master switch to disable group posting in case it is ever compromised

License
-------
All the technologies used here are free. You are subject to the licensing agreements of those service providers.

You are free to generally use this code as you please, as long as you don't blame me if it doesn't work (Please raise an issue, though, so I can fix it)
