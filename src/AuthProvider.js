import React, { Children, useState } from 'react';
import { AsyncStorage, Vibration } from 'react-native';
import basic_url from './baseUrl';
import axios from 'axios';
import { NavigationContainer } from '@react-navigation/native';

import registerForPushNotificationsAsync  from './PushNotification';
import { Notifications } from 'expo';


export const AuthContext = React.createContext({})


export const AuthProvider = ({children})=>{
    const [estudyToken, setUser] = useState(null);
    const [error, setError] = useState(null);
    
    return(
        <AuthContext.Provider value={{
            estudyToken,
            error,
            login:(username, password) =>{
                if (username && password){
                    axios.defaults.headers = {
                        'Content-Type': 'application/json',
                    }
                    axios.post(basic_url + 'login/', {
                        'username': username,
                        'password': password
                    }).then(res => {
                        const currentuser = res.data.token;
      
                        setUser(currentuser);
                        AsyncStorage.setItem('estudyToken', currentuser);
                        setError(false);

                        return registerForPushNotificationsAsync(res.data.token, res.data.id);
                        
                        

                    }).catch(err => {
                        console.log(err);
                        setError(true);
                    })
                }
            },
            logout:()=>{
                setUser(null);
                AsyncStorage.removeItem('estudyToken');
            },
            checkUserStatus:()=>{

                 // check user is loged in
                AsyncStorage.getItem('estudyToken').then(userString =>{
                    if(userString){
                        setUser(userString);
                    } 
                }).catch(err => {
                    console.log(err);
                    setUser(null);
                    AsyncStorage.removeItem('estudyToken');
                })
            }
        }}>
            {children}
        </AuthContext.Provider>
    )
}