import React, { useEffect, useState, useContext } from 'react';
import { Text, View, Button, Vibration, Platform } from 'react-native';
import { Notifications } from 'expo';
import * as Permissions from 'expo-permissions';
import Constants from 'expo-constants';
import axios from 'axios';
import basic_url from './baseUrl';
async function registerForPushNotificationsAsync(userToken, userId) {

        if (Constants.isDevice) {
          const { status: existingStatus } = await Permissions.getAsync(Permissions.NOTIFICATIONS);
          let finalStatus = existingStatus;
          if (existingStatus !== 'granted') {
            const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);
            finalStatus = status;
          }
          if (finalStatus !== 'granted') {
            alert('Failed to get push token for push notification!');
            return;
          }
          token = await Notifications.getExpoPushTokenAsync();
          if (Platform.OS === 'android') {
            Notifications.createChannelAndroidAsync('default', {
              name: 'default',
              sound: true,
              priority: 'max',
              vibrate: [0, 250, 250, 250],
            });
          }

          axios.defaults.headers = {
              'Authorization': "Token " + userToken,
              'Accept': '*/*',
              'Content-Type': 'application/json',
            }
          
          axios.patch(basic_url + 'student/update/profile/'+userId, {
              "notificationToken": token
          }).then(res => {
              // setData(res.data);
              // console.log(res.data);
              
          
          }).catch(err => {
              console.log(err);
              // logout();
          })
          
          
          const handleNotification = (notification) => {
            Vibration.vibrate();
            console.log(notification);
          }
        
          
          this.notificationSubscription = Notifications.addListener(handleNotification);
          
          
        } else {
          alert('Must use physical device for Push Notifications');
        }

      };
export default registerForPushNotificationsAsync;

