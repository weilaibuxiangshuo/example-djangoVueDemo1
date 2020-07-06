import {AddUserData,GetUserData,DelUserData} from "@/api/management/usermg"

const defaultState=()=>{
    return {
        username:"9999",
        routeIdVal:"",
    }
}
const state=defaultState()
const mutations={
    SET_ROUTE_ID:(state,val)=>{
        state.routeIdVal=val
    }
}
const actions={
    addUserData({commit},data){
        return new Promise((resolve,reject)=>{
            AddUserData(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    getUserData({commit},newObj){
        return new Promise((resolve,reject)=>{
            GetUserData(newObj).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    delUserData({commit},data){
        return new Promise((resolve,reject)=>{
            DelUserData(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    }
}

export default {
    namespaced:true,
    state,mutations,actions
}