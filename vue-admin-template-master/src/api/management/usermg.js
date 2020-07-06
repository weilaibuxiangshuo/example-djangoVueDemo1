import request from "@/utils/request"


// 添加
export function AddUserData(data){
    return request({
        url:"/mguser/",
        method:"post",
        data:data,
    })
}
// 获取用户
export function GetUserData(data){
    let currentpage=data.currentpage;
    let pagesize = data.pagesize;
    let search = data.search.trim();
    return request({
        url:`/getuser/${currentpage}/${pagesize}/`,
        method:"get",
        params:{"search":search},
    })
}

// 删除用户
export function DelUserData(data){
    return request({
        url:`/deluser/`,
        method:"delete",
        data:data
    })
}