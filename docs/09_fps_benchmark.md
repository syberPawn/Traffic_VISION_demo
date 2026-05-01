# FPS Benchmark

## Purpose

The demo uses uploaded video, but it must still report whether the processing pipeline is capable of real-time performance under the tested conditions.

The benchmark must not claim universal real-time capability.

## Required Metrics

Display:

- Input Video FPS.
- Input Video Duration.
- Total Frames Processed.
- Total Processing Time.
- System Processing FPS.
- Average Time Per Frame.
- Real-Time Factor.
- Real-Time Capability Status.

## Formulas

Input video duration:

```text
Input Video Duration = Total Input Frames / Input Video FPS
```

System processing FPS:

```text
System Processing FPS = Total Processed Frames / Total Processing Time
```

Average time per frame:

```text
Average Time Per Frame = Total Processing Time / Total Processed Frames
```

Real-time factor:

```text
Real-Time Factor = Input Video Duration / Total Processing Time
```

Real-time status:

```text
If System Processing FPS >= Input Video FPS:
    Real-time capable for this tested video and hardware
Else:
    Not fully real-time on this tested hardware
```

## Correct Wording

Use:

```text
The system processed the uploaded video at X FPS, while the source video frame rate was Y FPS. Since the measured processing FPS is greater than or equal to the source FPS, the system is capable of real-time processing under the tested video, hardware, resolution, and model configuration.
```

Do not use:

```text
The system is always real-time.
```

## Frame Skipping

Frame skipping is not part of the first implementation. If frame skipping is introduced later, the benchmark must clearly report:

- Total input frames.
- Frames actually processed.
- Frame skip interval.
- Effective processed FPS.

Do not compare skipped-frame processing FPS to full-frame video FPS without explaining the frame skip.

## Hardware Context

Where possible, display or document:

- CPU/GPU used.
- Whether CUDA is available.
- Model configuration.
- Input video resolution.

These affect benchmark interpretation.


