<template>
  <div id="databox">
    <div class="dataheader">
      <div class="firstheader">
        <el-form ref="form" :model="dataForm" label-width="80px">
          <el-form-item label="用户名称">
            <el-select v-model="dataForm.id" placeholder="请选择活动区域">
              <el-option
                :key="index"
                v-for="(value,index) in allUser"
                :label="value.username"
                :value="value.id"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="跳转目标">
            <el-input type="text" v-model="dataForm.target"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div class="secondheader">
        <el-button @click="addData" type="primary">添加域名</el-button>
        <div class="msgheader">
          <span>数量：{{dataForm.num}}</span>
          <span>剩余：{{dataForm.jumpnum==0?dataForm.num:dataForm.num-dataForm.jumpnum}}</span>
          <span>模式：{{dataForm.mode}}</span>
        </div>
        <div class="msgsearch">
          <el-input
            type="text"
            class="searchStyle"
            v-model="search"
            size="small"
            placeholder="域名搜索"
            clearable
            @change="serchPutChange"
          ></el-input>
          <el-button type="warning" icon="el-icon-search" size="small" @click="btnSearch" circle></el-button>
        </div>
      </div>
      <hr />
    </div>
    <div class="datamain">
      <!-- 对话框  -->
      <el-dialog
        :title="title==='NEW'?'添加域名':'编辑域名'"
        :visible.sync="dialogFormVisible"
        :before-close="handleClose"
      >
        <el-form :model="dialogform" ref="ruleForm" :rules="rules">
          <el-form-item label="域名" :label-width="formLabelWidth" prop="textinfo">
            <el-input
              type="textarea"
              v-model="dialogform.textinfo"
              autocomplete="off"
              :placeholder="placeholder"
              :rows="5"
              class="newtextarea"
            ></el-input>
          </el-form-item>
          <el-form-item label="目标" :label-width="formLabelWidth" v-if="isBtnTarget" prop="url">
            <el-input v-model="dialogform.url" placeholder="需添加 http://或https://"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancel">取 消</el-button>
          <el-button type="primary" @click="confirm">确 定</el-button>
        </div>
      </el-dialog>

      <el-table
        ref="multipleTable"
        :data="tableUserData"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" label="ID"></el-table-column>
        <el-table-column label="域名" prop="name"></el-table-column>
        <el-table-column label="目标" prop="jump"></el-table-column>
        <el-table-column align="right" label="地址">
          <template slot="header">
            <span class="spstyle">编辑</span>
          </template>
          <template v-slot="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
            >Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="datafooter">
      <div class="btnStyle">
        <el-button type="primary" icon="el-icon-share" @click="selectAllData">全选</el-button>
        <el-button type="primary" icon="el-icon-delete" class="btnDelStyle" @click="delAllData">全删</el-button>
      </div>
      <div class="paginationStyle">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagin.currentPage"
          :page-sizes="pagin.pagesizes"
          :page-size="pagin.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagin.total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>
<script>
const defaulutForm = {
  id: "",
  num: 0,
  mode: "",
  target: "",
  jumpnum: 0
};

const defaultDialogForm = {
  url: "",
  textinfo: ""
};

const defaultPagin = {
  currentPage: 1,
  pagesizes: [10, 20, 50],
  pagesize: 10,
  total: 10
};

export default {
  data() {
    const textinfoVali = (rule, value, callback) => {
      if (value.trim() === "") {
        return callback(new Error("请输入域名"));
      } else {
        return callback();
      }
    };
    const urlVali = (rule, value, callback) => {
      if (value.trim() === "") {
        return callback(new Error("请填写目标"));
      } else {
        let regEx = /^http.*?/;
        let res = regEx.test(value.toString().trim());
        if (res) {
          return callback();
        } else {
          return callback(new Error("格式不正确，请http://或https://开头"));
        }
      }
    };
    return {
      title: "NEW",
      search: "",
      routeId: this.$route.query.id,
      pagin: Object.assign({}, defaultPagin),
      currentUser: null,
      tableUserData: [],
      isBtnTarget: false,
      dataForm: Object.assign({}, defaulutForm),
      dialogform: Object.assign({}, defaultDialogForm),
      allUser: [],
      dialogFormVisible: false,
      formLabelWidth: "50px",
      placeholder:
        "可以单条、多条批量两种方式添加\r\n域名www和@只能选一种添加\r\n注：多条请以逗号或空格间隔",
      rules: {
        textinfo: [
          { required: true, validator: textinfoVali, trigger: "blur" }
        ],
        url: [{ required: true, validator: urlVali, trigger: "blur" }]
      }
    };
  },
  methods: {
    // 全选
    selectAllData() {
      this.$refs.multipleTable.toggleAllSelection();
    },
    // 全删
    delAllData() {
      const delAll = this.$refs.multipleTable.selection;
      if (delAll.length) {
        let newD = new Array();
        for (let n = 0; n < delAll.length; n++) {
          newD.push({ id: delAll[n].id });
          this.$store
            .dispatch("datamg/delJumps", JSON.stringify(newD))
            .then(response => {
              this.pagin.total -= 1;
              this.getAllJumps();
            });
        }
      } else {
        return false;
      }
    },
    handleSelectionChange(val) {
      // console.log(val)
      this.multipleSelection = val;
    },
    // 当前显示的页数
    handleSizeChange(val) {
      let isR = val * this.pagin.currentPage > this.pagin.total;
      if (isR) {
        this.pagin.pagesize = val;
        this.handleCurrentChange(1);
        return false;
      }
      this.pagin.pagesize = val;
      this.getAllJumps();
    },
    // 当前页码
    handleCurrentChange(val) {
      this.pagin.currentPage = val;
      this.getAllJumps();
    },
    handleEdit(index, row) {
      if (this.dataForm.id.toString().trim() === "") {
        return false;
      }
      this.title = "EDIT";
      let numMode = parseInt(this.dataForm.mode);
      if ([2, 6].indexOf(numMode) !== -1) {
        this.isBtnTarget = true;
        this.dialogform.url = row.jump;
        this.dialogform.textinfo = row.name;
        this.dialogFormVisible = true;
      } else {
        this.isBtnTarget = false;
        return false;
      }
    },
    handleDelete(index, row) {
      let newD = new Array();
      newD.push({ id: row.id });
      this.$store
        .dispatch("datamg/delJumps", JSON.stringify(newD))
        .then(response => {
          // console.log(response);
          this.pagin.total -= 1;
          this.getAllJumps();
        });
    },
    // 添加目标
    addData() {
      if (this.dataForm.id.toString().trim() === "") {
        return false;
      }
      let numMode = parseInt(this.dataForm.mode);
      if ([2, 6].indexOf(numMode) !== -1) {
        this.isBtnTarget = true;
      } else {
        this.isBtnTarget = false;
      }
      this.title = "NEW";
      this.dialogFormVisible = true;
    },
    // 确定送出
    confirm() {
      this.$refs["ruleForm"].validate(vali => {
        if (!vali) {
          return false;
        } else {
          let str = this.dialogform.textinfo.toString();
          if (str.trim() == "") {
            return false;
          }
          if (this.isBtnTarget) {
            let strUrl = this.dialogform.url.toString();
            if (strUrl.trim() == "") {
              return false;
            }
          }
          this.dialogFormVisible = false;
          let strUrl = this.dialogform.url.toString();
          // let reg = /([0-9a-zA-Z\.\-]+)?(\s|,|$)/g;
          let reg = /.*?(\s|,|$)/g;
          const strList = str.match(reg);
          let dialogList = [];
          for (let i = 0; i < strList.length; i++) {
            let temp = strList[i].trim();
            if (temp === "" || temp === ",") {
              delete strList[i];
            } else {
              // 判断后是否有逗号
              let exp = strList[i].substr(-1, 2);
              if (exp === ",") {
                exp = strList[i].substr(0, strList[i].length - 1);
                dialogList.push(exp);
              } else {
                dialogList.push(strList[i]);
              }
            }
          }
          const newL = {
            id: this.dataForm.id,
            mode: this.dataForm.mode,
            textarea: dialogList,
            url: strUrl
          };
          let newF = new FormData();
          newF.append("data", JSON.stringify(newL));
          this.$store.dispatch("datamg/addUserData", newF).then(response => {
            // console.log(response);
            this.getAllJumps();
            this.clearTextarea();
          });
        }
      });
    },
    getAllUsers() {
      this.$store.dispatch("datamg/getUserData").then(response => {
        this.allUser = response.data;
        const routeId = this.$store.getters.routeIdVal;
        if (this.$route.query.id && this.$route.query.id == routeId) {
          this.dataForm.id = parseInt(this.$route.query.id);
        } else {
          this.$router.push({ path: this.$route.path });
        }
      });
    },
    // 获取所有目标
    getAllJumps() {
      if (this.currentUser === null) {
        return false;
      }
      if (
        (this.pagin.currentPage - 1) * this.pagin.pagesize ==
          this.pagin.total &&
        this.pagin.currentPage - 1 > 0
      ) {
        this.pagin.currentPage -= 1;
      }
      let newObj = {
        currentpage:
          this.pagin.currentPage === null ? 1 : this.pagin.currentPage,
        pagesize: this.pagin.pagesize
      };
      const newSerVal = this.search.toString().trim();
      const temp = {
        id: this.currentUser,
        pgObj: newObj,
        search: newSerVal === "" ? "" : newSerVal
      };
      this.$store.dispatch("datamg/getAllJumps", temp).then(response => {
        this.tableUserData = response.data;
        this.pagin.total = response.total;
        this.dataForm.jumpnum = response.total;
      });
    },
    // 取消对话框
    cancel() {
      this.dialogFormVisible = false;
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.$refs["ruleForm"].resetFields();
    },
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.$refs["ruleForm"].resetFields();
      done();
    },
    // 清除对话框内容
    clearTextarea() {
      this.dialogform = Object.assign({}, defaultDialogForm);
    },
    // 按下搜索时触发
    btnSearch() {
      this.getAllJumps();
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
      let newVal = val.toString().trim();
      if (newVal == "") {
        this.getAllJumps();
      }
    }
  },
  created() {
    this.getAllUsers();
  },
  mounted() {},
  watch: {
    "dataForm.id": function(val) {
      // console.log(val);
      for (let m in this.allUser) {
        if (this.allUser[m].id === val) {
          this.dataForm.id = this.allUser[m].id;
          this.dataForm.target = this.allUser[m].target;
          this.dataForm.num = this.allUser[m].num;
          this.dataForm.jumpnum = this.allUser[m].jumpnum;
          this.dataForm.mode = eval(this.allUser[m].mode)[0];
          this.currentUser = val;
          this.getAllJumps();
        }
      }
    }
  }
};
</script>
<style scoped>
.dataheader {
  margin: 10px 0px 0px 20px;
}
.datamain {
  margin-left: 22px;
}

.el-select {
  display: block;
}
.el-button {
  margin-left: 0px;
}
.secondheader {
  margin-left: 10px;
}
.msgheader {
  display: inline-block;
  margin-left: 30px;
}
.msgheader span:nth-child(2) {
  margin-left: 10px;
  color: red;
}
.msgheader span:last-child {
  margin-left: 10px;
}
.btnStyle {
  display: inline-block;
  margin-top: 20px;
  margin-left: 30px;
  vertical-align: middle;
}

.paginationStyle {
  margin-top: 20px;
  margin-left: 30px;
  display: inline-block;
  vertical-align: middle;
}

.btnDelStyle {
  background-color: #f56c6c;
  border-color: #f56c6c;
}

.spstyle {
  margin-right: 61px;
}

.searchStyle {
  width: 200px;
  margin-left: 20px;
}

.msgsearch {
  display: inline-block;
}
</style>