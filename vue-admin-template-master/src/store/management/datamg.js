import {GetUserData,AddUserData,GetAllJumps,DelJumps} from "@/api/management/datamg"

const defaultState=()=>{
    return{
        "datalist":""
    }
}

const state=defaultState()

const mutations={}
const actions={
    // 获取用户
    getUserData({commit},data){
        return new Promise((resolve,reject)=>{
            GetUserData(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    // 添加目标
    addUserData({commit},data){
        return new Promise((resolve,reject)=>{
            AddUserData(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    // 获取目标
    getAllJumps({commit},data){
        return new Promise((resolve,reject)=>{
            GetAllJumps(data).then(response=>{
                resolve(response)
            })
        })
    },
    // 删除目标
    delJumps({commit},data){
        return new Promise((resolve,reject)=>{
            DelJumps(data).then(response=>{
                resolve(response)
            })
        })
    }
}

export default {
    namespaced: true,
    state,mutations,actions
}