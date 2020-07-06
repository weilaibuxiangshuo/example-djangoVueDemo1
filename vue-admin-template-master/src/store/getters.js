const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  routeIdVal:state=>state.usermg.routeIdVal,
  defaultRoute:state=>state.user.defaultRoute,
  roleVal:state=>state.user.role,
  userid:state=>state.user.userid,
}
export default getters
