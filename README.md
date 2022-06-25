# congenial-spork

# Multi Faces Analysis Pipeline Demo {#ovms_demo_multi_faces_analysis_pipeline}


This document demonstrates how to create complex pipelines using object detection and object recognition models from OpenVINO Model Zoo. As an example, we will use [face-detection-retail-0004](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/face-detection-retail-0004/README.md) to detect multiple faces on the image. Then, for each detected face we will crop it using [model_zoo_intel_object_detection](https://github.com/openvinotoolkit/model_server/tree/releases/2022/1/src/custom_nodes/model_zoo_intel_object_detection) example custom node. Finally, each image face image will be forwarded to [age-gender-recognition-retail-0013](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/age-gender-recognition-retail-0013/README.md) and [emotion-recognition-retail-0003](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/emotions-recognition-retail-0003/README.md) models.



Using such a pipeline, a single request to OVMS can perform a complex set of operations to determine all faces and their properties.

### See also

For simpler use case with single face analysis see [single_face_analysis_pipeline](../../single_face_analysis_pipeline/python/README.md) demo.

## Pipeline Configuration Graph

Below is depicted graph implementing faces analysis pipeline execution. 



It includes the following Nodes:
- Model `face-detection` - deep learning model which takes user image as input. Its outputs contain information about face coordinates and confidence levels.
- Custom node `model_zoo_intel_object_detection` - it includes C++ implementation of common object detection models results processing. By analysing the output it produces cropped face images based on the configurable score level threshold. Custom node also resizes them to the target resolution and combines into a single output of a dynamic batch size. The output batch size is determined by the number of detected
boxes according to the configured criteria. All operations on the images employ OpenCV libraries which are preinstalled in the OVMS. Learn more about the [model_zoo_intel_object_detection custom node](https://github.com/openvinotoolkit/model_server/tree/releases/2022/1/src/custom_nodes/model_zoo_intel_object_detection).
- demultiplexer - outputs from the custom node model_zoo_intel_object_detection have variable batch size. In order to match it with the sequential recognition models, data is split into individuial images with each batch size equal to 1.
Such smaller requests can be submitted for inference in parallel to the next Model Nodes. Learn more about the [demultiplexing](../../../docs/demultiplexing.md).
- Model `age-gender-recognition` - this model recognizes age and gender on given face image
- Model `emotion-recognition` - this model outputs emotion probability for emotions: neutral, happy, sad, surprised and angry
- Response - the output of the whole pipeline combines the recognized face images with their metadata: coordinates, age, gender, emotions and detection confidence level. 

## Prepare workspace to run the demo

To successfully deploy face analysis pipeline you need to have a workspace that contains:
- [face-detection-retail-0004](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/face-detection-retail-0004/README.md), 
[age-gender-recognition-retail-0013](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/age-gender-recognition-retail-0013/README.md) and
[emotion-recognition-retail-0003](https://github.com/openvinotoolkit/open_model_zoo/blob/2022.1.0/models/intel/emotions-recognition-retail-0003/README.md) models
- Custom node for image processing
- Configuration file

Clone the repository and enter multi_faces_analysis_pipeline directory
```bash
git clone https://github.com/openvinotoolkit/model_server.git
cd model_server/demos/multi_faces_analysis_pipeline/python
```

You can prepare the workspace that contains all the above by just running

```
make
```

### Final directory structure

Once the `make` procedure is finished, you should have `workspace` directory ready with the following content.
```
workspace
├── age-gender-recognition-retail-0013
│   └── 1
│       ├── age-gender-recognition-retail-0013.bin
│       └── age-gender-recognition-retail-0013.xml
├── config.json
├── emotion-recognition-retail-0003
│   └── 1
│       ├── emotions-recognition-retail-0003.bin
│       └── emotions-recognition-retail-0003.xml
├── face-detection-retail-0004
│   └── 1
│       ├── face-detection-retail-0004.bin
│       └── face-detection-retail-0004.xml
└── lib
    └── libcustom_node_model_zoo_intel_object_detection.so
```

## Deploying OVMS

Deploy OVMS with faces analysis pipeline using the following command:

```bash
docker run -p 9000:9000 -d -v ${PWD}/workspace:/workspace openvino/model_server --config_path /workspace/config.json --port 9000
```

go to fluffy winner


