import React, { useState, useEffect, useContext } from 'react';
import { NavigationContainer} from "@react-navigation/native";
import {View, ActivityIndicator, AsyncStorage,StyleSheet} from "react-native";
import { AuthContext } from './AuthProvider';
import { AppTabs } from './AppTabs';
import { AuthStack } from './AuthStack';


 const Routes = ({}) => {
    const {estudyToken, login, checkUserStatus} = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [userLogedIn, setUserLogedIn] = useState(false);

    useEffect(() => {
        checkUserStatus();
        setLoading(false);
        // setUserLogedIn()
    },[])
    if(loading){
        return(
            <View style = {styles.container}><ActivityIndicator size="large"></ActivityIndicator></View>
    )
    };
    return (
        <NavigationContainer>
            {estudyToken ? <AppTabs/> : <AuthStack/>}
            {/* <AppTabs /> */}
        </NavigationContainer>
    );
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
  
}});

export default Routes;