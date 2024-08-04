# A-EYE 👀✏️📙
Need help improving your studying? A-EYE is an innovative study helper using **eye-tracking** technology and **facial recognition** to analyze an individual's _study productivity_.

## Inspiration
Studying in different environments can significantly impact focus and productivity. We were inspired to analyze if we could determine a student's optimal environment that yields the highest productivity score over a period of time using image analysis. To do this, we wanted students to be able to track their study sessions with A-EYE which will generate a report after the session denoting how focused the student was throughout the session.

## What it does
Our project uses eye-tracking technology and facial recognition to analyze an individual's study productivity. The system calculates an arbitrary "focus" score over a time frame of 10-20 seconds, using weights derived from scientific research studies. Constantly changing gaze, facial expression can denote poor concentration while looking up for long periods can denote good concentration. Once the study session ends, the user receives a chart showing their focus level over time and an overall productivity score.

## How we built it
We built the project using the following technologies:
- **Frontend**: Angular
- **Backend**: Django + MongoDB
- **Image Analysis**: Python, OpenCV, DeepFace, GazeTracking

The frontend captures images from video and sends them to the backend. We then use gaze tracker and deepface to process each image, aggregating 5 images in a 10 second window to determine characteristics like frequent glancing, change in emotions or constant neutral expression and gaze. For each window, a focus score is produced using heuristics obtained from the research papers. After the study session ends, the frontend fetches the processed windows and displays the result as a graph to the user.

## Challenges we ran into
- Integrating various technologies (Angular, Django, OpenCV, DeepFace) into a cohesive system
- Ensuring accurate and reliable gaze tracking and facial recognition
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

## Limitations
- Hard to distinguish between certain actions like person looking down when thinking or looking at their paper vs when person is looking at their phone (assuming phone is out of frame)
- Arbitrary weights could yield innacurate results since every student's behavior is different
- Eye gaze model not 100% accurate which could lead to discrepancies in the data collected
- Multiple faces could be detected

## What's next for AEYE
- Enhancing the accuracy and reliability of the gaze tracking and facial recognition components
- Implementing user feedback to improve the focus algorithm as every student exhibits different behaviors when studying
- Ensure privacy by processing data onsite vs on the server
- Batch processing on the fly with queue and map-reduce for performance and scalability

## References
1. [Analysis of Learners' Emotions in E-Learning Environments Based on Cognitive Sciences](https://www.researchgate.net/publication/380588073_Analysis_of_Learners'_Emotions_in_E-Learning_Environments_Based_on_Cognitive_Sciences)
2. [Gaze direction as a facial cue of memory retrieval state](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1063228/full)
