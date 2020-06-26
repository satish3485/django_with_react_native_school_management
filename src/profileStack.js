import React, { useEffect, useState, useContext  } from 'react';
import { createStackNavigator, HeaderTitle } from '@react-navigation/stack';
import {View, Text, StyleSheet, TouchableOpacity, Image,  Modal, ScrollView, ImageBackground, Alert } from "react-native";
import { FlatList, TouchableHighlight, TextInput } from 'react-native-gesture-handler';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';
import basic_url from './baseUrl';
import colors from './colors';
import { AuthContext } from './AuthProvider';
import { Card, Icon } from 'react-native-elements';

const Stack = createStackNavigator();




function ViewProfile({navigation}){
    const {estudyToken, logout} = useContext(AuthContext);
    const [data, setData] = useState([]);
    const [userImage, setUserImage] = useState('../assets/student/student.png');
    const [studentId, setStudentId] = useState('');
    const [studentClass, setStudentClass] = useState('');
    const [passwordChangeModel, setPasswordChangeModel] = useState(false);
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState();
    useEffect(() => {

        const token = "Token " + estudyToken;

        axios.defaults.headers = {
            "Content-Type": "application/json",
            Authorization: token
        }
        axios.get(basic_url + 'student/profile').then(res => {
            setData(res.data);
            setStudentId(res.data.id)
            setUserImage(res.data.image+'?'+Math.random())

        }).catch(err => {
            console.log(err);
            logout();
        })

        axios.defaults.headers = {
            "Content-Type": "application/json",
            Authorization: token
        }

        axios.get(basic_url + 'student/class').then(res => {
            setStudentClass(res.data.name +' '+res.data.section);
            
        }).catch(err => {
            console.log(err);
            logout();
        })

    },[]);
    // const pickImage = () =>{}
    const pickImage = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.3,
          base64: true,
        });
    
        
    
        if (!result.cancelled) {
            setUserImage(result.uri);
            const token = "Token " + estudyToken;

            axios.defaults.headers = {
                
                'Authorization': token,
                // 'Content-Type': 'multipart/form-data;boundary="another cool boundary"',
                'Accept': '*/*',
                
            }
            
            // 'image': (result.base64 == undefined) ? result.uri : result.base64
            axios.patch(basic_url + 'student/update/profile/'+ studentId, {
                'image': result.base64
            }).then(res => {
                setData(res.data);
                
                
            }).catch(err => {
                console.log(err);
                logout();
            })
        }
      };

      const onbtnSavePress = () => {
        if(newPassword.length < 8){
            setError("Password lenght should be more than 8 !")
            return
        }
        else if(newPassword != confirmPassword){
            setError("Password does not match !")
            return
        }
        else{
            const token = "Token " + estudyToken;
            axios.defaults.headers = {
                
                'Authorization': token,
                'Accept': '*/*',
                'Content-Type': 'application/json'
            }
            
            axios.patch(basic_url + 'student/changepassword/'+ studentId, {
                'old_password': currentPassword,
                'new_password': newPassword
            }).then(res => {
                console.log("Password changed successfully !");
                setPasswordChangeModel(false);
            }).catch(err => {
                console.log(err);
                setError("Wrong Password !")
            })
        }
      }




    return(
        <ScrollView>
        <View style={styles.container}>
        <View>
            <Modal  transparent={false} visible={passwordChangeModel} >
                <View >
                    <View >
                        <View style={styles.modalContainer}>
                        <View style={styles.modalHeader}>
                            <Text style={styles.title}>Change Password</Text>
                            <View style={styles.divider}></View>
                        </View>
                        <View style={styles.modalBody} >
                        {error && <Text style = {styles.errorText} > {error} </Text>}

                            <View style={[styles.bottomView,{backgroundColor:"white"}]}>
                                <View style={styles.inputView}>
                                    <TextInput style={styles.inputText} placeholder="Current Password"
                                    multiline={false} placeholderTextColor={"#3c3c3c"} autoCorrect={false} underlineColorAndroid={'transparent'}  secureTextEntry={true} onChangeText={(e) => setCurrentPassword(e)} value={currentPassword}></TextInput>
                                </View>
                                <View style={styles.inputView}>
                                    <TextInput style={styles.inputText} placeholder="NewPassword"
                                        multiline={false} placeholderTextColor={"#3c3c3c"} autoCorrect={false} underlineColorAndroid={'transparent'}  secureTextEntry={true} onChangeText={(e) => setNewPassword(e)} value={newPassword}></TextInput>
                                </View>
                                <View style={styles.inputView}>
                                    <TextInput style={styles.inputText} placeholder="Confirm Password"
                                        multiline={false} placeholderTextColor={"#3c3c3c"} autoCorrect={false} underlineColorAndroid={'transparent'}  secureTextEntry={true} onChangeText={(e) => setConfirmPassword(e)} value={confirmPassword}></TextInput>
                                </View>
                                <View style={styles.rowInItem}>
                                    <TouchableOpacity style={styles.btnSave} activeOpacity={0.6} onPress={() => onbtnSavePress()}>
                                        <Text style={styles.textSave} numberOfLines={1}> Save</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity style={styles.btnCancel} 
                                        onPress={() => {
                                            setPasswordChangeModel(!passwordChangeModel); setError(null)
                                        }}>
                                        <Text style={styles.actionText}>Cancel</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </View>
                </View>
            </View>
        </Modal>
        </View>
        <TouchableOpacity onPress={pickImage}>
            <View style={styles.headerContainer}>
                
                <ImageBackground style={styles.headerBackgroundImage} blurRadius={10}
                    source={{ uri: userImage }} >
                    <View style={styles.headerColumn}>
                        <Image style={styles.userImage} source={{ uri: userImage }} />
                        <Text style={styles.userNameText}>{data.name}</Text>
                        <View style={styles.userAddressRow}>
                        <View>
                            <Icon
                            name="place"
                            underlayColor="transparent"
                            iconStyle={styles.placeIcon}
                            />
                        </View>
                        <View style={styles.userCityRow}>
                            <Text style={styles.userCityText}>
                            {data.address}
                           
                            </Text>
                        </View>
                        </View>
                    </View>
                    </ImageBackground>
                </View>
                </TouchableOpacity>
            <View style={styles.bodyContent}>
            <View style={styles.menuBox}>
            <View style={styles.icon}><Text style={styles.boxTextStyle}>{studentClass}</Text></View>
                <Text style={styles.info}>Class</Text>
              </View>
              <View style={styles.menuBox}>
              <View style={styles.icon}><Text  style={styles.boxTextStyle}>{data.gender}</Text></View>
              <Text style={styles.info}>Gender</Text>
              </View>
              </View>


            <View style={styles.listItem}>
                <View style={styles.iconStyle}>
                    <Icon name='male' type='fontisto' color='#517fa4' />
                </View>
                <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{data.fatherName}</Text>
                </View>
            </View>
            <View style={styles.listItem}>
                <View style={styles.iconStyle}>
                    <Icon name='female' type='fontisto' color='#517fa4' />
                </View>
                <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{data.motherName}</Text>
                </View>
            </View>
            <View style={styles.listItem}>
                <View style={styles.iconStyle}>
                    <Icon name='phone' type='fontisto' color='#517fa4' />
                </View>
                <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{data.phone}</Text>
                </View>
            </View>
            <View style={styles.listItem}>
                <View style={styles.iconStyle}>
                    <Icon name='email' type='fontisto' color='#517fa4' />
                </View>
                <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{data.email}</Text>
                </View>
            </View>
            
            <View style={styles.listItem}>
                <View style={styles.iconStyle}>
                    <Icon name='date' type='fontisto' color='#517fa4' />
                </View>
                <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{data.dateofbirth}</Text>
                </View>
            </View>
            <View style={styles.rowInItem}>
            <TouchableOpacity onPress={() => setPasswordChangeModel(true)}>
                <View style={styles.logoutButtonItem}>
                    <View style={styles.iconStyle}>
                        <Icon name='refresh' type='simple-line-icon' color='#517fa4' />
                    </View>
                    <Text style={styles.textWithIconStyle}>Change Password</Text>
                </View>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => logout()}>
                <View style={styles.logoutButtonItem}>
                    <View style={styles.iconStyle}>
                        <Icon name='login' type='simple-line-icon' color='#517fa4' />
                    </View>
                    <Text style={styles.textWithIconStyle}>Log Out</Text>
                </View>
            </TouchableOpacity>
            </View>
            </View>
        </ScrollView>
    )
}



export const ProfileStack =() => {
    return(
        <Stack.Navigator screenOptions={{
            headerTitleAlign: 'center',
            }}>
            <Stack.Screen name="viewprofile" component={ViewProfile} options={{headerTitle:"Profile"}} />
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
      justifyContent:'center',
      alignItems:'center',
      overflow: "scroll",
      flexDirection: 'column'
      
    },

    cardContainer: {
        backgroundColor: '#FFF',
        borderWidth: 0,
        flex: 1,
        margin: 0,
        padding: 0,
      },
      container: {
        flex: 1,
      },
      emailContainer: {
        backgroundColor: '#FFF',
        flex: 1,
        paddingTop: 30,
      },
      headerBackgroundImage: {
        paddingBottom: 20,
        paddingTop: 35,
      },
      headerContainer: {},
      headerColumn: {
        backgroundColor: 'transparent',
        alignItems: 'center',
       
      },
      placeIcon: {
        color: 'white',
        fontSize: 26,
      },
      scroll: {
        backgroundColor: '#FFF',
      },
      telContainer: {
        backgroundColor: '#FFF',
        flex: 1,
        marginHorizontal: 5,
        paddingTop: 30,
      },
      userAddressRow: {
        alignItems: 'center',
        flexDirection: 'row',
      },
      userCityRow: {
        backgroundColor: 'transparent',
      },
      userCityText: {
        color: '#ffffff',
        fontSize: 15,
        fontWeight: '600',
        textAlign: 'center',
      },
      userImage: {
        borderColor: '#01C89E',
        borderRadius: 85,
        borderWidth: 3,
        height: 170,
        marginBottom: 15,
        width: 170,
      },
      userNameText: {
        color: '#FFF',
        fontSize: 22,
        fontWeight: 'bold',
        paddingBottom: 8,
        textAlign: 'center',
      },

      menuBox:{
        backgroundColor: "#DCDCDC",
        width:120,
        height:100,
        alignItems: 'center',
        justifyContent: 'center',
        margin:10,
        shadowColor: 'black',
        shadowOpacity: .2,
        shadowOffset: {
          height:2,
          width:-2
        },
        elevation:4,
      },
      icon: {
        height:70,
        alignItems:'center',
        justifyContent:'center',
        alignSelf:'center',
        overflow:'hidden'
      },
      info:{
        fontSize:22,
        color: "#696969",
        bottom:0
      },
      bodyContent: {
        flex: 1,
        alignItems: 'center',
        padding:30,
      },
      bodyContent:{
        paddingTop:10,
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent:'center',
        alignItems:'center',
        alignSelf:'center'
      },
      textInsideBox:{
          alignSelf:'center',
          alignItems:'center',
          justifyContent:'center'
      },
      boxTextStyle:{
          fontSize: 30,
          textTransform:'uppercase'
        //   fontWeight:400
      },
      listItem:{
        margin:5,
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
            fontSize: 15,
            fontWeight: "bold",
            textTransform:'capitalize'
    },
    iconStyle:{
        justifyContent:'center',
        alignItems:'center',
        alignSelf:'center',
        marginLeft:5
    },
    logoutButtonItem:{
        margin:5,
        padding:10,
        backgroundColor:"#FFF",
        // width:"35%",
        flex:2,
        alignSelf:"center",
        borderRadius:25,
        alignItems:'center',
        justifyContent:'center',
        flexDirection:'row'
    },
    textWithIconStyle:{
        padding:7
    },
    rowInItem:{
        // flex:1,
        flexDirection:'row',
        alignItems:'center',
        justifyContent:'center'
    },
    modal:{
        backgroundColor:"#00000099",
        flex:1,
        alignItems: 'center',
        justifyContent: 'center',

      },
      modalContainer:{
        backgroundColor:"#f9fafb",
        width:"100%",
        borderRadius:5,
      },
      modalHeader:{
        justifyContent: 'center',
        alignItems:'center',
        alignSelf:'center'
      },
      title:{
        fontWeight:"bold",
        fontSize:20,
        padding:15,
        color:"#000"
      },
      divider:{
        width:"100%",
        height:1,
        backgroundColor:"lightgray"
      },
      modalBody:{
        backgroundColor:"#fff",
        paddingVertical:20,
        paddingHorizontal:10
      },

      actions:{
        borderRadius:5,
        marginHorizontal:10,
        paddingVertical:10,
        paddingHorizontal:20
      },
      actionText:{
        color:"#fff"
      },
      bottomView: {
        backgroundColor: 'white',
    },
    inputText: {
        paddingVertical: 5,
        color: '#3c3c3c',
        marginLeft: 10,
        fontSize: 14,
        textAlign: 'left'
    },
    inputView:{
        backgroundColor: 'white',
        borderRadius: 5,
        justifyContent: 'flex-start',
        borderWidth: 1,
        marginHorizontal: 10,
        marginVertical: 10,
        borderColor: '#3c3c3c',
        overflow: 'hidden',
    },
    btnSave: {
        backgroundColor: '#00ACC1',
        paddingHorizontal: 30,
        height: 30,
        justifyContent: 'center',
        borderRadius: 15,
        overflow: 'hidden',
        alignSelf: 'center',
        marginTop: 15
    },

    textSave: {
        alignSelf: 'center',
        color: 'white',
        fontSize: 16,
        textAlign: 'center',
        marginHorizontal: 5
    },
    errorText: {
        color: 'red',
        fontSize: 15,
        height: 20,
        borderColor: 'red',
        borderWidth: 0,
        alignSelf:'center'
      },
      btnCancel:{
        backgroundColor:"#db2828", 
        margin: 4,
        paddingHorizontal: 30,
        height: 30,
        justifyContent: 'center',
        borderRadius: 15,
        overflow: 'hidden',
        alignSelf: 'center',
        marginTop: 15
        }
    
})