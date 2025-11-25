# Gesture-Based Painting in the Air

A real-time virtual drawing application that lets you **paint in mid-air using hand gestures** captured through your webcam. Built using **Python, OpenCV, and MediaPipe**, this project transforms your hand movements into brush strokes on a digital canvas, no physical contact needed.

---

## Features

* **Hand Gesture Recognition** using MediaPipe
* **Air Drawing** with index finger
* **3 Different color Selection Panel** (Red, Blue, Green, Eraser)
* **Dynamic Brush Size Control** using finger distance
* **Eraser Mode** for clearing strokes
* **Clear Canvas Gesture**
* Real time performance

---

## Gesture Controls

To select your color simply hover your index finger over the desired option while in selection mode.
To lift your finger from the air canvas, any gesture other than the below is suitable. You can also use selection mode to move without drawing.

| Gesture                                                                                                                                   | Action                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Index finger up                                                                                                                           | Draw mode                                                                 |
| Index + Middle up                                                                                                                         | Selection mode (choose color)                                             |
| Thumb + Index + Pinky up  \n(you can dynamically adjust by making a pinching like gesture by thumb and index finger with pinky finger up) | Brush size control – distance between thumb and index determines the size |
| All fingers down (closed fist)                                                                                                            | Clear canvas                                                              |

---

## Requirements to Run

Install the following Python libraries:

```bash
pip install opencv-python mediapipe numpy
```

Ensure you have:

* Python 3.7+
* A working webcam

---

## Running the Application

1. Clone or download this repository
2. Navigate into the folder:

```bash
cd Gesture-Based-Painting-in-the-Air
```

3. If dependencies are installed in Anaconda (otherwise skip this step):

```bash
conda activate mp
```

4. Run the program:

```bash
python virtual_painter.py
```

Press **Q** in the application to terminate.

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy

---

## Link to our PPT and GitHub Repository

PPT: [https://www.canva.com/design/DAG2htx5WFg/5kvHt7A8pJDi5sKr1lgaZQ/view?utm_content=DAG2htx5WFg&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h1e204b6b0f](https://www.canva.com/design/DAG2htx5WFg/5kvHt7A8pJDi5sKr1lgaZQ/view?utm_content=DAG2htx5WFg&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h1e204b6b0f)

* GitHub Repo: [https://github.com/prar1hana/Gesture-Based-Painting-in-the-Air](https://github.com/prar1hana/Gesture-Based-Painting-in-the-Air)

---
