# seeknspot

# Inspiration
As university students diving into advanced coursework, we are frequently met with extensive and highly technical lecture videos. We all have different learning styles and capabilities. Navigating these lectures to pinpoint specific information can be a daunting task. Recognizing this challenge, we were motivated to develop a tool that could automatically pinpoint content within these videos.

In addition, in the age of video media, we wanted to create a tool for those with visual and hearing impairments, so the content of these videos can be accessible to anyone.

But our vision goes beyond just academia. We envision a transformation in content consumption – be it pinpointing a memorable scene in a movie, identifying a character in a series, or revisiting cherished personal memories. Our application is poised to redefine efficiency in accessing ideas and knowledge.

# What it does
Our solution is a Chrome extension tailored for YouTube videos. Once activated, the extension assesses the content of the video and provides a platform for users to pose questions. Based on the video's content, it supplies answers, complete with timestamps indicating the source of the information, and will redirect the video to the relevant timestamp with a click of a button. It is very adaptive, allowing for translations and analysis of videos in any language. This ensures that no matter where the user is located in the world or their background, they will be able to effectively understand and engage with the video's content.

That is just the beginning of SeekNSpot's capabilities. Beyond that, we go a step further by summarizing key points of the video, presenting them in an easily accessible format. For those wanting to test their grasp on the content, it also offers an interactive quiz feature. Advanced users enjoy a very granular level of customization with our application, being able to fine-tune the AI model parameters, allowing for precise results. By leveraging advanced AI algorithms and multilingual support, our extension breaks down barriers, making YouTube videos more comprehensible, interactive, and universally accessible to users from all walks of life. In essence, we aim to transform passive video watching into an active, personalized, and enriching learning experience.

# Target Audience
While students stand to benefit immensely from our platform, it's essential to note that our tool caters to a much broader audience. Whether you're watching a video for academic, professional, or recreational purposes, our application dives deeper, enhancing the viewing experience. We've taken significant strides in ensuring our platform is universally accessible. This includes accommodating non-native English speakers, individuals with visual or auditory impairments, and those with cognitive or attention-related challenges. We've restructured video content into a more digestible format, empowering users to interact and engage with content at a pace that suits them best. From professionals seeking clarity to enthusiasts exploring new realms or those needing content tailored to specific accessibility requirements, our platform resonates with and aids every unique viewer. Our mission? To democratize information access and ensure learning is a seamless journey for everyone.

# How we built it
Our extension is a full-stack application. The frontend, crafted using Streamlit, presents an intuitive user interface written in Python. To conform to Chrome's extension standards, this frontend is channeled through a JavaScript window, allowing ideal integration with websites. Communication lines are maintained with a Flask backend, responsible for cataloging video content and other pertinent data.

We take advantage of the llama-2 model, alongside the Replicate API to deliver the most reliable responses. In addition, to create a secure environment we utilize Auth0, which makes logging in and out of the application seamless.

# Challenges we ran into
Navigating the constraints of Chrome extensions posed a significant challenge. Given the mandate for extensions to operate client-side only, we innovated a solution integrating HTML and JavaScript for the display, while the StreamLit and Flask components handle the core logic.

Additionally, real-time video transcription presented a hurdle due to its computational demands. To counter this, we tapped into YouTube's API for transcripts. These transcripts, segmented by timestamps, became the foundation for contextual question-answering.

# Accomplishments that we're proud of
Our biggest accomplishment was being able to get our AI bot to accurately answer our questions, as well as redirect to the relevant part of the video to support the answer. Fine-tuning its ability to correctly address questions and guide users to video segments for further context required several iterations and solution strategies. We're proud of having developed a robust system capable of managing a myriad of scenarios.

# What we learned
This project served as a deep dive into AI model training and refinement. Beyond the technical aspects, it refined our skills in project design and execution. The journey enriched our knowledge in project management, team collaboration, and crafting intricate solutions from the ground up.

# What's next for SeekNSpot
The horizon is teeming with potential enhancements for SeekNSpot. We plan to expand our platform to be compatible with any video player, regardless of content. A high-priority addition on our radar is a video annotation feature, empowering users to make notes on videos and share insights with the broader community. An ambitious goal we have is to incorporate image analysis, allowing our AI to provide insights into visual elements within videos – from scribbles on a whiteboard to identifying the video's location or setting. We're super excited to take SeekNSpot to the next level!

# Built With
AI
Auth0
CSS
Flask
HTML
JavaScript
LLM
Llama-2
Python
Replicate
Streamlit

# To Run
Flask Server: python backend.py <br />
Streamlit App: streamlit run llama2_chatbot.py <br />
Chrome Extension: Load unpack the seeknspot_chrome_extension folder on extensions under Chrome

# Link to Live Demo
