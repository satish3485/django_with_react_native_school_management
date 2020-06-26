import React, { useEffect, useState, useContext  } from 'react';
import { createStackNavigator, HeaderTitle } from '@react-navigation/stack';
import {View, Text, StyleSheet, TouchableOpacity, Image,  ScrollView } from "react-native";
import { FlatList } from 'react-native-gesture-handler';
import ImageView from 'react-native-image-view';
import axios from 'axios';
import basic_url from './baseUrl';
import colors from './colors';
import { AuthContext } from './AuthProvider';
import { Card, Icon } from 'react-native-elements';


const Stack = createStackNavigator();

// ===============dummy data ==============

// const Data = [{"id":14,"name":"math","school":1,"clas":16,"teacher":null},{"id":15,"name":"science","school":1,"clas":16,"teacher":null},{"id":16,"name":"social science","school":1,"clas":16,"teacher":null}]

// const Assignemtss = [{"id":20,"name":"assignments1","description":"sdfafsdsds sdsd  trtrrttrtrtrtrtrrttrrt  trtrrt   rttrt rt  tr tt trtrrt   trtr tr  t    trrttrt r trtrtrtr  tr trtr  trtr tr sd sd sd sd sd sd  sd dsff d fd fd f df d f dfdf f dfd df f d fd f d fd f fd ff d df dfd fd f d ff dfd  df  df df ee r re er re  rere  re  re re er er  frtregr grtgrgrtgergterhtgertgrtgger e g er g rthg rerge rgerh rtg r g rt grthrt h rt hrt grt ","startDate":"2020-06-15","endDate":"2020-06-06","image":'https://cdn.pixabay.com/photo/2017/08/17/10/47/paris-2650808_960_720.jpg',"maxPoints":20,"course":16},{"id":21,"name":"assignments1","description":"sdfafs","startDate":"2020-06-15","endDate":"2020-06-06","image":null,"maxPoints":20,"course":16},{"id":22,"name":"assignments1","description":"sdfafs","startDate":"2020-06-15","endDate":"2020-06-06","image":null,"maxPoints":20,"course":16},{"id":23,"name":"assignments1","description":"sdfafs","startDate":"2020-05-04","endDate":"2020-06-06","image":null,"maxPoints":20,"course":16}]

// ==========================================


const data = []
function Item({ item, navigation }) {

    const [color, setColor] = useState('');
    useEffect(() => {
        const randomN =  Math.round(Math.random() * 220);
        setColor(colors[randomN]);
    },[])
    return (
        <TouchableOpacity onPress={()=> navigation.navigate("assignment",{
            object:item
        })}>
                <View style={styles.listItem}>
                    <Image source={require('../assets/book_image.png') }  
                    style={{width:60, height:60,borderRadius:30}} />
                    <View style={styles.eachItem}>
                    <Text  style={styles.eachItemText}>{item.name}</Text>
                    </View>
                </View>
        </TouchableOpacity>
    );
    }

function AssignmentsList({ item, navigation }) {
    const [color, setColor] = useState('');
    useEffect(() => {
        const randomN =  Math.round(Math.random() * 220);
        setColor(colors[randomN]);
    },[])
    return (
        <TouchableOpacity onPress={()=> navigation.navigate("assignmentDetail",{
            object:item
        })}>
                <View style={styles.listItem}>
                    <Image source={require('../assets/book_image.png') }  
                    style={{width:60, height:60,borderRadius:30}} />
                    <View style={styles.eachItem}>
                        <Text  style={styles.eachItemText}>{item.name}</Text>
                        <View style={styles.itemInRow}>
                            <View  style={styles.eachItemStartDateButton} ><Icon name='date' type='fontisto' color='#00af00' /><Text>{item.startDate}</Text></View>
                            <View  style={styles.eachItemEndDateButton} ><Icon name='date' type='fontisto' color='#d70000' /><Text>{item.endDate}</Text></View>
                        </View>
                    </View>
            </View>
        </TouchableOpacity>
    );
    }

function GetSubjects({ navigation }){
    const {estudyToken, logout} = useContext(AuthContext);
    const [data, setData] = useState([]);


    useEffect(() => {
        
        const token = 'Token ' + estudyToken;
        // navigation.addListener ('willFocus', () =>
        // // run function that updates the data on entering the screen
        //  console.log( "i am in home page")
        // );
        axios.defaults.headers = {
            'Authorization': token,
            'Content-Type': 'text/plain',
            'Accept': '*/*',
            
        }
        axios.get(basic_url + 'course/').then(res => {
            setData(res.data);
            
        }).catch(err => {
            console.log(err);
            logout();
        })

    },[])

    return(
        <View style={styles.container}>
        <FlatList
          style={{flex:1}}
          data={data}
          renderItem={({ item }) => <Item item={item} navigation = {navigation}/>}
          keyExtractor={item => item.id.toString()}
        />
      </View>
    )
    
}

function Assignment({route, navigation}){
    const [data, setData] = useState([]);
    const {estudyToken, logout} = useContext(AuthContext);

    useEffect(() => {
        const token = "Token " + estudyToken;

        axios.defaults.headers = {
            // "Content-Type": "application/json",
            Authorization: token,
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data'
        }
        axios.get(basic_url + 'assignments/'+route.params.object.id).then(res => {
            setData(res.data);
            
        }).catch(err => {
            console.log(err.code);
            logout();
        })

    },[])
    
    return(
        <View style={styles.container}>
        <FlatList
          style={{flex:1}}
          data={data}
          renderItem={({ item }) => <AssignmentsList item={item} navigation = {navigation}/>}
          keyExtractor={item => item.id.toString()}
        />
      </View>
    )
}


function AssignmentDetail({route, navigation}){
    const [isImageVisible, setisImageVisible] = useState(false);
    const images = [{source: {uri: route.params.object.image},width: 806,height: 720}];

    return(
        <ScrollView >
        <View style={styles.container}>
            <Card title={route.params.object.name} titleStyle={{textTransform:'capitalize', fontStyle:'italic', fontSize:20}}>
                <View style={styles.itemInRow2}>
                    <View  style={styles.maxPointsFields} ><Text style={{fontSize:20, padding:7}}>{route.params.object.maxPoints}</Text></View>
                   
                    <View  style={styles.eachItemStartDateButton} ><Icon name='date' type='fontisto' color='#00af00' /><Text>{route.params.object.startDate}</Text></View>
                    <View  style={styles.eachItemEndDateButton} ><Icon name='date' type='fontisto' color='#d70000' /><Text>{route.params.object.endDate}</Text></View>
                </View>
                <Card title="Description" containerStyle={{width:"105%", marginHorizontal:0, alignSelf:'center',justifyContent:'center'}}  titleStyle={{textTransform:'capitalize', fontStyle:'italic', fontSize:20}}>
                <View>
                    <Text style={{fontSize:20}}>{route.params.object.description}</Text>
                </View>
                </Card>
                <TouchableOpacity style={styles.imagePrevuewButton} onPress={() => {setisImageVisible(true)}}><Text style={{fontSize:15}}>Attachments</Text></TouchableOpacity>
            
                <ImageView images={images} imageIndex={0} isVisible={isImageVisible} onClose={() => {setisImageVisible(false)}}/>
            </Card>
            
        </View>
        </ScrollView>
    )
}


export const HomeStack =() => {
    return(
        <Stack.Navigator screenOptions={{
            headerTitleAlign: 'center',
            }}>
            <Stack.Screen name="subjects" component={GetSubjects} options={{headerTitle:"Subjects"}}  />
            <Stack.Screen name="assignment" component={Assignment} options={{headerTitle:"Assignments"}} />
            <Stack.Screen name="assignmentDetail" component={AssignmentDetail} />
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
      marginLeft: 2
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

},
itemInRow2:{
    alignSelf:'center',
    alignItems:'center',
    flexDirection:'row',
    // marginLeft: 2,
    justifyContent:'space-between',
    width:'100%',


},

  });