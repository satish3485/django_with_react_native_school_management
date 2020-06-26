import React from 'react';
import { createBottomTabNavigator} from "@react-navigation/bottom-tabs";
import { View,Text} from 'react-native';
import {Ionicons } from '@expo/vector-icons';
import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { HomeStack } from './HomeStack';
import { ProfileStack } from './profileStack';
import {AllAssignmentStack} from './AllAssignmentStack';
import { NotificationStack } from './NotificationStack';

const Tabs = createBottomTabNavigator();


export const AppTabs= ({}) => {
    return (
        <Tabs.Navigator 
        screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;
  
              if (route.name === 'Home') {
                iconName = 'md-home';
              } else if (route.name === 'Assignments') {
                return <MaterialIcons name="assignment" size={size} color={color} />
              }
              else if (route.name === 'Notification') {
                return <Ionicons name="ios-notifications-outline" size={size} color={color} />
              }
              else if (route.name === 'Profile') {
                return <MaterialCommunityIcons name="account-circle-outline" size={size} color={color} />
              }
  
              // You can return any component that you like here!
              return <Ionicons name={iconName} size={size} color={color} />;
            },
          })}
          tabBarOptions={{
            activeTintColor: 'tomato',
            inactiveTintColor: 'gray',
          }}>
            <Tabs.Screen name="Home" component={HomeStack}></Tabs.Screen>
            <Tabs.Screen name="Assignments" component={AllAssignmentStack}></Tabs.Screen>
            <Tabs.Screen name="Notification" component={NotificationStack}></Tabs.Screen>
            <Tabs.Screen name="Profile" component={ProfileStack}></Tabs.Screen>
        </Tabs.Navigator>

    );
}

