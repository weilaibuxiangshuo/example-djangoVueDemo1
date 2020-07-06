
export function DeepClone(func){
    let  newType = func.constructor==Object?{}:[];
    for(let key in func){
        if(func[key]&&typeof(func[key])==="object"){
            newType[key]=DeepClone(func[key])
        }else{
            newType[key]=func[key]
        }
    }
    return newType
}
