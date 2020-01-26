# PixReader

#Running
To run this project you will need to create a .env file with the definitions for 'GOOGLE_APPLICATION_CREDENTIALS' and 'MICROSOFT_CV_SUBSCRIPTION_KEY'.
These can be obtained by setting up a Google Cloud project and a Microsoft Azure project.

#Inspiration
I wanted to create an assistive technology that was more robust than what's currently available. Web developers don't always provide alt-text for their images and I wanted to create an alternative to depending on alt-text.

#What it does
PixReader is an assistive screen reader that reads text and auto-generated captions for images with the help of computer vision!

#How I built it
This was built with Microsoft Cognitive Services (Describe Image), Google Cloud Text-to-Speech, and all strung together with python3.

#Challenges I ran into
I initially tried to build the screen reader portion of the project with Google's Web Speech API, but there's minimal documentation for it and the only resource I could find was a blog post translated from Polish. Additionally, after implementing Microsoft Cognitive Services for the image caption generation, I tried to use Google's "im2text" model because I was impressed by its superior results. Sadly, all the pre-trained models I found online were sub-par and training it myself, even with my GPU, would take weeks. Not a luxury provided by TAMUhack.

#Accomplishments that I'm proud of
I was in an unfortunate seating arrangement where I needed to stay where I was to use the ethernet cable and didn't really have room for teammates to join me, so I'm proud that I finished something so lofty both by myself and so quickly!

#What I learned
I learned how to use Google Cloud Text-to-Speech and Microsoft Cognitive Services!

#What's next for PixReader
Hopefully an improved model for the image caption generation!
