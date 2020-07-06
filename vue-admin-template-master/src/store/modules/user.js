import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter,newRoutes,constantRoutes } from '@/router'
import {sha256} from 'js-sha256'
import {DeepClone} from '@/utils/newmg'
import Layout from '@/layout'
import path from 'path'
import {setrole,setuser} from "@/utils/auth"
const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    defaultRoute:constantRoutes,
    role:"",
    userid:"",
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROUTE:(state,data)=>{
    state.defaultRoute = constantRoutes.concat(data)
  },
  SET_ROLE:(state,data)=>{
    state.role = data
  },
  SET_USERID:(state,id)=>{
    state.userid = id
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    let oneForm = new FormData()
    oneForm.append("data",JSON.stringify({ username: username.trim(), password: password.trim() }))
    return new Promise((resolve, reject) => {
      login(oneForm).then(response => {
        if(response.token){
          commit('SET_TOKEN', response.token)
          setToken(response.token)
        }
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const {username,roles,code,userid} = response
        commit('SET_NAME', username)
        commit('SET_ROLE',roles)
        commit('SET_USERID',userid)
        // setrole(roles)
        // setuser(username)
        let newR = DeepClone(newRoutes)
        let ff = changeRoute(newR,"/",1,roles)
        commit('SET_ROUTE',ff)
        resolve(ff)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

    // error logout
    errorout({ commit, state }) {
      removeToken() 
      resetRouter()
      commit('RESET_STATE')
    },



  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

const changeRoute =(newR,dfPath,num,newRoute)=>{
  const newObj = newR.constructor === Array?[]:{}
  for(let mm in newR){
    let nbj = newR[mm]
    let dic = {}
    const newPath = path.join(dfPath,nbj.path)
    if(nbj&&nbj.constructor===Object){
      if(nbj.hidden){continue}
      if(nbj.meta&&nbj.meta.roles){
        let role = nbj.meta.roles
        if(role.indexOf(newRoute) !== -1){
          dic["meta"] = nbj.meta
        }else{
          continue
        }
      }
      if(nbj.redirect){
        dic["redirect"]=nbj.redirect
      }
      if(nbj.name){
        dic["name"]=nbj.name
      }
      if(nbj.children){
        if(nbj.children.length===0){continue}
        if(nbj.children.length>0){
          dic["path"]=nbj.path;
          dic["component"]=num===1?Layout:resolve => require([`@/views${newPath}`],resolve);
          dic["children"]=changeRoute(nbj.children,nbj.path,2,newRoute)
          if(dic["children"].length===0){
            continue
          }
        }
      }else{
        dic["path"]=nbj.path;
        dic["component"]=num===1?Layout:resolve => require([`@/views${newPath}`],resolve);
      }
      // 如果用等号，列表会出现empty
      newObj.push(dic)
    }
  }
  return newObj
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}


