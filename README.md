**Project Title:** Stove and Fire Safety Monitoring System

**Objective:** Enhance home fire safety by detecting the status of a stove (on/off) and the presence of a fire simultaneously. Ensure that the stove is actively used for cooking when turned on, and promptly alert users in case of potential dangers.

**Key Features:**

1. **Stove Status Detection:** Utilizes YOLO-8 algorithm for real-time object detection to recognize the state of the stove (on/off). This ensures that the system can accurately identify whether the stove is in use or not.

2. **Fire Detection:** Monitors the area around the stove for the presence of fire using image analysis and computer vision techniques. The system must promptly identify any flames or fire sources.

3. **Safety Mode:** When the stove is on, and a fire is actively detected, the system indicates "Safe Mode," ensuring that the stove is being used for cooking purposes safely.

4. **Danger Mode:** If the stove is on, but no fire is detected for a certain continuous period (e.g., 120 frames), the system switches to "Danger Mode" to alert users about the potential risk. It calculates a percentage to reflect the level of risk based on the duration without fire detection.

5. **Threshold Alert:** Provides a customizable threshold for danger mode detection, allowing users to define when they consider the stove as potentially unsafe based on their preferences.

6. **Real-time Monitoring:** The system operates in real-time, continuously analyzing the stove area to provide immediate feedback.

**Benefits:** 

- Increases home fire safety by reducing the risk of unattended stoves causing accidents.
- Empowers users with an automated safety monitoring system that provides real-time alerts.
- Customizable danger mode threshold enables users to adjust sensitivity based on their preferences.


## Tech Stack

**Language:** Python

**Libraries to Use:** CVZone,Cv2,Ultralytics

**UI:** StreamLit

**Model to Use:** Finetuned Yolo-V8 Small Model with Custom Dataset


## Run Locally

Clone the project

```bash
git clone https://github.com/Sathishmahi/Fire-Detection.git
```

create ,activate conda env and install requirements   

```bash
 bash init_setup.sh 
```
run streamlit app

```bash
bash run.sh
```

## Demo Video

https://github.com/Sathishmahi/Fire-Detection/assets/88724458/7ed43e03-b5e2-4ad4-b190-ff652e19a441


