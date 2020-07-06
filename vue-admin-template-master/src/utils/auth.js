import Cookies from 'js-cookie'

const TokenKey = 'token-csrf-auth'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

const rolekey = "role-auth"

export function getrole(){
  return Cookies.get(rolekey)
}

export function setrole(val){
  return Cookies.set(rolekey,val)
}

export function removerole(){
  return Cookies.get(rolekey)
}


const userkey = "user-auth"

export function getuser(){
  return Cookies.get(userkey)
}

export function setuser(val){
  return Cookies.set(userkey,val)
}

export function removeuser(){
  return Cookies.get(userkey)
}
