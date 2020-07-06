import Vue from "vue"
import router from "@/router"

const hass = Vue.directive('hass',{
    inserted:function(el,binding,vnode){
        if(binding.value==="subuser"){
            el.parentNode.removeChild(el)
        }
    }
})

const edithass = Vue.directive('edithass',{
    inserted:function(el,binding,vnode){
        if(binding.value==="subuser"){
            el.style.marginRight = "28px"
        }
    }
})

const mainhass = Vue.directive('mainhass',{
    inserted:function(el,binding,vnode){
        if(binding.value==="subuser"){
            el.style.marginLeft = "0px"
        }
    }
})

export {hass,edithass,mainhass}