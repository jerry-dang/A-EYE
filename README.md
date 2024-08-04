# A-EYE
Need help improving your studying? AEYE is an innovative study helper using **eye-tracking** technology and **facial recognition** to analyze an individual's _study productivity_.

## Inspiration
Studying in different environments can significantly impact focus and productivity. We were inspired to analyze if we could determine an optimal environment that yields the highest productivity score over a period of time using image analysis. By leveraging eye-tracking technology and facial recognition, we aimed to create an innovative study helper that provides insights into an individual's study productivity.

## What it does
Our project uses eye-tracking technology and facial recognition to analyze an individual's study productivity. The system calculates an arbitrary "focus" score over a time frame of 10-20 seconds, using weights derived from scientific research studies. The user receives a chart showing their focus level over time and an overall productivity score after ending their study session.

## How we built it
We built the project using the following technologies:
- **Frontend**: Angular
- **Backend**: Django with MongoDB
- **Image Analysis**: Python scripts using OpenCV, DeepFace, and gaze tracking

The frontend captures images from video and sends them to the backend. The backend aggregates data from the gaze tracker and facial recognition model, creating an object that holds this information in a queue based on timestamps. After the study session ends, the backend processes the images sequentially and calculates the focus score.

## Challenges we ran into
- Integrating various technologies (Angular, Django, OpenCV, DeepFace) into a cohesive system
- Ensuring accurate and reliable gaze tracking and facial recognition
- Managing the large volume of image data and processing it efficiently, including binary and base64 conversions
- Creating meaningful, logical and scientifically-backed weights for the focus score calculation

## Accomplishments that we're proud of
- Successfully integrating eye-tracking and facial recognition technologies to analyze study productivity
- Developing a system that provides real-time feedback on focus levels
- Creating an innovative tool that has the potential to help individuals optimize their study environments and improve productivity

## What we learned
- The importance of seamless integration between frontend and backend technologies
- Techniques for effective gaze tracking and facial recognition
- How to process and analyze large volumes of image data efficiently
- The value of using scientific research to inform our focus score calculations

## What's next for AEYE
- Enhancing the accuracy and reliability of the gaze tracking and facial recognition components
- Expanding the system to analyze additional factors that may affect study productivity, such as lighting and background noise
- Implementing user feedback to improve the overall user experience and cater to specific user habits and needs
- Add authentication along with unique user IDs in order for the product to be scalable 
