import React, {useContext, useState } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import {View, Text, Button, StyleSheet, Image,TextInput,TouchableOpacity,Keyboard} from "react-native";
import { AuthContext } from './AuthProvider';
import axios from 'axios';
import { AsyncStorage } from 'react-native';
import basic_url from './baseUrl';
import { hasPrefixSuffix } from 'antd/lib/input/ClearableLabeledInput';
import { AppTabs } from './AppTabs';

const Stack = createStackNavigator();

const initialStateUsername = ''

function Login({navigation}){
    function validateForm() {
      return username.length > 0 && password.length > 0;
    }
 
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = useState('');
    const {login, error} = useContext(AuthContext);
  
    return (
        <View style = {styles.container} >
          <Image style = {styles.logo}
            source = {
              require('../assets/logo.png')
            }/> 

       {error && <Text style = {styles.errorText} > Please check your username and password! </Text>}

       <TextInput style = { styles.inputBox }
        underlineColorAndroid = 'rgba(0,0,0,0)'
        placeholder = "Username"
        placeholderTextColor = "#1126be"
        selectionColor = "#fff"
        keyboardType = "default"
        onChangeText={text => setUsername(text)} />
        <TextInput style = {styles.inputBox}
          underlineColorAndroid = 'rgba(0,0,0,0)'
          placeholder = "Password"
          secureTextEntry = {true}
          placeholderTextColor = "#1126be"
          onChangeText={e => setPassword(e)} />
          <TouchableOpacity style = {styles.button} onPress={()=> login(username, password)}><Text style = {styles.buttonText} > Login </Text>  
          </TouchableOpacity >
          <TouchableOpacity><Text style = {styles.forgetButton}
            onPress={()=> navigation.navigate("forgetPassword")} > Forget Password ? </Text> 
          </TouchableOpacity >
    </View>
    )
}

function ForgetPassword({navigation}){
  const {logout} = useContext(AuthContext);
    return (
        <View>
            <TextInput ></TextInput>
            <Text>I am in forgetPassword view</Text>
            <Button title="login" onPress={()=> navigation.navigate("login")}> Login</Button>
       
        </View>
    )
}

function Logout({navigation}){
  const {logout} = useContext(AuthContext);
  logout();
    return (
        <View>
            <TextInput ></TextInput>
            <Text>I am in log out</Text>
            <Button title="logout" onPress={()=> navigation.navigate("login")}> Login</Button>
        </View>
    )
}


export const AuthStack = ({}) => {
    return (
        <Stack.Navigator screenOptions={{
            header:()=> null
        }} initialRouteName="login">
            <Stack.Screen name="login" component={Login} />
            <Stack.Screen name="forgetPassword"  component={ForgetPassword} />
            <Stack.Screen name="logout"  component={Logout} />
        </Stack.Navigator>
    )
}


const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#fefefe',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
  
  
    },
    logo: {
      width: 100,
      height: 100,
      marginBottom: 30
    },
  
    inputBox: {
      width: 300,
      backgroundColor: 'rgba(255, 255,255,0.2)',
      borderBottomWidth: 2,
      paddingHorizontal: 16,
      fontSize: 20,
      marginVertical: 20,
      height: 50,
      color: '#1126be'
    },
    button: {
      width: 200,
      backgroundColor: '#1126be',
      borderRadius: 25,
      marginVertical: 10,
      paddingVertical: 13,
      height: 50
    },
    buttonText: {
      fontSize: 20,
      fontWeight: '500',
      color: '#ffffff',
      textAlign: 'center',
      textAlign: "center"
    },
    forgetButton: {
      color: '#1126be'
    },
    signupTextCont: {
      alignItems: 'flex-end',
      justifyContent: 'center',
      paddingVertical: 16,
      flexDirection: 'row',
    },
    signupText: {
      fontSize: 16
    },
    signupButton: {
      color: '#1126be',
      fontSize: 20,
      fontWeight: '500'
    },
    errorText: {
      color: 'red',
      fontSize: 10,
      height: 20,
      borderColor: 'red',
      borderWidth: 0
    },
  
  
  });