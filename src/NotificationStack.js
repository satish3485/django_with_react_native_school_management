import React, { useEffect, useState, useContext  } from 'react';
import { createStackNavigator, HeaderTitle } from '@react-navigation/stack';
import {View, Text, StyleSheet, TouchableOpacity, RefreshControl, Image,  Modal, ScrollView, ImageBackground, Alert } from "react-native";
import { FlatList, TouchableHighlight, TextInput } from 'react-native-gesture-handler';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';
import basic_url from './baseUrl';
import colors from './colors';
import { AuthContext } from './AuthProvider';
import { Card, Icon } from 'react-native-elements';
import {Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
const Stack = createStackNavigator();

function AllNotificationsList({ item, navigation }) {
    const [color, setColor] = useState('');
    useEffect(() => {
        const randomN =  Math.round(Math.random() * 220);
        if(item.unread) {
            setColor(colors[randomN]);
        }
        
    },[])
    return (
        <TouchableOpacity onPress={()=> navigation.navigate("readnotification",{
            object:item
        })}>
                <View style={styles.listItem }>
                    {/* <Image source={require('../assets/book_image.png') }  
                    style={{width:60, height:60,borderRadius:30}} /> */}
                    <Text style={{justifyContent:'center', alignItems:'center',alignSelf:'center', marginLeft:15}}><Ionicons name="ios-notifications-outline" size={40} color="green"/></Text>
                    
                    <View style={styles.eachItem}>
                        <Text  style={styles.eachItemText}>{item.verb}</Text>
                        {/* <View style={styles.itemInRow}>
                         <Text >{item.description}</Text>
                        </View> */}
                    </View>
            </View>
        </TouchableOpacity>
    );
    }

function ReadNotification({route, navigation}){
    const {estudyToken, logout} = useContext(AuthContext);
    const [data, setData] = useState();
    
    useEffect(() => {
        const token = "Token " + estudyToken;
        axios.defaults.headers = {
                
            'Authorization': token,
            "Content-Type": "application/json",
            'Accept': '*/*',
            
        }
        
        axios.patch(basic_url + 'inbox/notifications/update/'+route.params.object.id , {
            "unread": false
        }).then(res => {
            setData(res.data);
 
            
        }).catch(err => {
            console.log(err);
            logout();
        })
        
    },[])

    return(
        <ScrollView >
        <View style={styles.container}>
            <Card title={route.params.object.verb} titleStyle={{textTransform:'capitalize', fontStyle:'italic', fontSize:20}}>
                
                <Card title="Detail" containerStyle={{width:"105%", marginHorizontal:0, alignSelf:'center',justifyContent:'center'}} titleStyle={{textTransform:'capitalize', fontStyle:'italic', fontSize:20}}>
                <View>
                    <Text style={{fontSize:20}}>{route.params.object.description}</Text>
                </View>
                </Card>

            </Card>
            
        </View>
        </ScrollView>
    );
}

function wait(timeout) {
    return new Promise(resolve => {
      setTimeout(resolve, timeout);
    });
  }
  

function ViewNotifications({navigation}){
    const [data, setData] = useState([]);
    const {estudyToken, logout} = useContext(AuthContext);
    const [refreshing, setRefreshing] = React.useState(false);

    const onRefresh = React.useCallback(() => {
        setRefreshing(true);
        // const token = "Token " + estudyToken;
        // axios.defaults.headers = {
        //     // "Content-Type": "application/json",
        //     Authorization: token
        // }
        // axios.get(basic_url + 'inbox/notifications/').then(res => {
        //     setData(res.data);
            
            
        // }).catch(err => {
        //     console.log(err.code);
        // });
        
    
        wait(2000).then(() => setRefreshing(false));
      }, [refreshing]);

    useEffect(() => {
  
        
        const token = "Token " + estudyToken;
        axios.defaults.headers = {
            // "Content-Type": "application/json",
            Authorization: token
        }
        axios.get(basic_url + 'inbox/notifications/').then(res => {
            setData(res.data);
            
            
        }).catch(err => {
            console.log(err.code);
        });

    },[])

    return(

        <View style={styles.container}>
            {/* <ScrollView contentContainerStyle={{flex:1}}
                > */}
                <FlatList
                style={{flex:1}}
                data={data}
                refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} /> }
                renderItem={({ item }) => <AllNotificationsList item={item} navigation = {navigation}/>}
                keyExtractor={item => item.id.toString()}
                />
            {/* </ScrollView> */}
        </View>
      
    )
  }

export const NotificationStack =() => {
    return(
        <Stack.Navigator screenOptions={{
            headerTitleAlign: 'center',
            }}>
            <Stack.Screen name="viewnotification" component={ViewNotifications} options={{headerTitle:"Notifications"}} />
            <Stack.Screen name="readnotification" component={ReadNotification} options={{headerTitle:"Notifications"}} />
        </Stack.Navigator>
    )
}

const styles = StyleSheet.create({
    container: {
    //   flex: 'flex-start',
      flex: 1,
      backgroundColor: '#F7F7F7',
      marginTop:10,
      width: "100%",
      height: "100%",

      overflow: "scroll",
      flexDirection: 'column'
      
    },
    listItem:{
      margin:15,
      padding:10,
      backgroundColor:"#FFF",
      width:"95%",
      flex:1,
      alignSelf:"center",
      flexDirection:"row",
      borderRadius:25,
    },
    eachItem:{
        alignItems:"center", 
        flex:1,
        justifyContent:"center",

    },
    eachItemText:{
        alignItems:"center", 
        textAlign:"center",
        justifyContent:"center",
        fontSize: 25,
        fontWeight: "bold",
        textTransform:'capitalize'
 },
 title:{
     alignSelf:"center",
    alignItems:"center", 
    justifyContent:"center",
    width: "95%",
    borderWidth:2,
    borderRadius:25,
    textTransform:'capitalize'

 },

  scrollViewP: {
    justifyContent:"center",
    alignItems:"center",
    alignSelf:"center",
    marginTop:10,
    borderWidth:2,
    borderRadius:25,
    width:"95%",
    flex:1,
  },
  eachItemStartDateButton:{
    // backgroundColor:'#5fffaf',
    borderColor:'#00af00',

    padding:2,

    marginLeft:10,
  },
  eachItemEndDateButton:{
    // backgroundColor:'#d70000',
    borderColor:'#d70000',

    padding:2,

    marginLeft:20,
  },
  itemInRow:{
      alignSelf:'center',
      flexDirection:'row',
      marginLeft: 2,
      justifyContent:'center',
      width:'100%'

  },
  itemInRow2:{
    alignSelf:'center',
    alignItems:'center',
    flexDirection:'row',
    // marginLeft: 2,
    justifyContent:'space-between',
    width:'100%',


},
  eachItemDateButtonMargin:{
    borderWidth:4,
    borderRadius:25,
    padding:4,
    alignSelf:'flex-start',
    marginLeft:10,
    width: '95%',
    alignItems: "center",
    marginVertical: 10
  },
  assignmentFile:{
    // flex:1,
    width:"100%",
    height:"100",
    alignSelf: 'center'
  },
  scrollView: {
    alignSelf:"center",
    alignItems:"center", 
    justifyContent:"center",
   
  },
  imagePrevuewButton:{
      width:120,
      borderRadius:25,
      justifyContent: 'center',
      alignSelf: 'center',
      alignItems: 'center',
      padding: 10,
      marginVertical: 10,
      backgroundColor:'#e7e7e7',
      flex:1
  },
  imagePrewiewStyle:{
    //   flex: 1,
      width: 807,
  },
  maxPointsFields:{
      borderWidth:4,
      width:60,
      height:60,
      borderRadius: 30,
      borderColor:'yellow',
      justifyContent:'center',
      alignItems:'center',
      alignSelf:'center',
      backgroundColor:'yellow'
    //   marginHorizontal: 20

  }

  });