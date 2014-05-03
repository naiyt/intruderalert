intruderalert
=============

An SL4A script to be used w/Tasker to alert you of unauthorized access to your Android device.

If someone puts in an incorrect PIN into your Android device, this will take pictures of the intruder, and email them to your email of choice. There are apps that do this, but I like setting it up with Tasker instead. It means you get a LOT more flexibility with what you can do, and the images/emails never go through a third party. (Er, besides whatever your email provider is.) You can take as many pictures as you want, from both the front and back cameras, and at any resolution that they support. You have full access to the subject and body of the emails. Additionally, you could have it do other cool stuff, like turn on the GPS, and snag the phone's coordinates as well, or send a text to someone, or upload the images to your DropBox. Ultimately, if you know what you're doing, I think it's more fun and rewarding to do this with Tasker than with an app made for this kind of thing.

This runs off of two profiles. One monitors for incorrect PINs, and takes the pictures. It checks to see if it has an internet connection available -- if not, it stores the images in a temporary directory. The second profile checks every 10 minutes to see if there are any unsent images. If so, it tries to send them. If it can, it deletes the images. If not, it will just try again in another 10 minutes.

I'll try to get instructions and the profiles committed shortly as well.