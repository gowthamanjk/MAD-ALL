import React, { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { RNCamera } from 'react-native-camera';

const App = () => {
  const [barcode, setBarcode] = useState(null);
  const [processedData, setProcessedData] = useState(null);

  const handleBarcodeRead = async (scanResult) => {
    const { data } = scanResult;
    setBarcode(data);


    try {
      const response = await fetch('http://<your-server-ip>/process_barcode', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ barcode: data }),
      });

      const result = await response.json();
      setProcessedData(result);
    } catch (error) {
      console.error('Error processing barcode:', error);
    }
  };

  return (
    <View style={styles.container}>
      <RNCamera
        style={styles.camera}
        type={RNCamera.Constants.Type.back}
        onBarCodeRead={handleBarcodeRead}
        captureAudio={false}
      >
        <View style={styles.overlay}>
          {barcode && <Text style={styles.barcodeText}>Scanned Barcode: {barcode}</Text>}
        </View>
      </RNCamera>
      {processedData && (
        <View style={styles.resultContainer}>
          <Text>Processed Data: {processedData.result}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  camera: {
    flex: 1,
    width: '100%',
    justifyContent: 'flex-end',
  },
  overlay: {
    position: 'absolute',
    top: '10%',
    left: '5%',
    right: '5%',
    bottom: '10%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  barcodeText: {
    fontSize: 20,
    color: 'white',
  },
  resultContainer: {
    marginTop: 20,
    padding: 20,
    backgroundColor: 'lightgrey',
    borderRadius: 10,
  },
});

export default App;
