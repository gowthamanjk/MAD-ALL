import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, TouchableOpacity } from 'react-native';

const App = () => {
  const [fontSize, setFontSize] = useState(16);
  const [color, setColor] = useState('black');
  const [fontFamily, setFontFamily] = useState('System');

  const changeStyle = () => {
    setFontSize(fontSize === 16 ? 24 : 16); // Toggle font size
    setColor(color === 'black' ? 'blue' : 'black'); // Toggle color
    setFontFamily(fontFamily === 'System' ? 'serif' : 'System'); // Toggle font family
  };

  return (
    <View style={styles.container}>
      <Text style={[styles.text, { fontSize, color, fontFamily }]}>
        This is the text
      </Text>
      <TouchableOpacity onPress={changeStyle} style={styles.button}>
        <Text style={styles.buttonText}>Change Text Style</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#007bff',
    padding: 10,
    borderRadius: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
});

export default App;
