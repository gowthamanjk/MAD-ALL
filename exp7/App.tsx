import React, { useState } from 'react';
import { View, Button, Image, Text } from 'react-native';
import { launchCamera } from 'react-native-image-picker';

const App = () => {
  const [imageUri, setImageUri] = useState(null);
  const [imageData, setImageData] = useState(null);

 
  const captureImage = () => {
    const options = {
      mediaType: 'photo',
      cameraType: 'back',
      quality: 0.8,
    };
    launchCamera(options, (response) => {
      if (response.didCancel) {
        console.log('User canceled image picker');
      } else if (response.errorCode) {
        console.log('ImagePicker Error: ', response.errorMessage);
      } else {
        setImageUri(response.assets[0].uri);
      
      }
    });
  };


  const sendImageToBackend = (uri) => {
    const formData = new FormData();
    formData.append('image', {
      uri,
      type: 'image/jpeg',
      name: 'image.jpg',
    });

    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => setImageData(data))
      .catch((error) => console.error('Error:', error));
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Button title="Capture Image" onPress={captureImage} />
      {imageUri && (
        <View style={{ marginTop: 20 }}>
          <Image
            source={{ uri: imageUri }}
            style={{ width: 200, height: 200, borderRadius: 10 }}
          />
          {imageData && <Text>{imageData.result}</Text>}
        </View>
      )}
    </View>
  );
};

export default App;
