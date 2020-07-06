import request from "@/utils/request"


export function GetUserData(data){
    return request({
        url:"/getdata/",
        method:"get",
        params:data
    })
}

export function AddUserData(data){
    return request({
        url:"/jpdata/",
        method:"post",
        data:data,
    })
}

export function GetAllJumps(data){
    return request({
        url:`/getjpdata/${data.pgObj.currentpage}/${data.pgObj.pagesize}/`,
        method:"get",
        params:data.search==""?{"userId":data.id}:{"userId":data.id,"search":data.search}
    })
}

export function DelJumps(data){
    return request({
        url:`/deljpdata/`,
        method:"delete",
        data:data
    })
}