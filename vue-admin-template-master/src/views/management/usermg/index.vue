<template>
  <div id="mgbox">
    <div class="mgheader">
      <el-button @click.native.prevent="dialogFormVisible = true">添加用户</el-button>
      <div class="msgsearch">
          <el-input
            type="text"
            class="searchStyle"
            v-model="search"
            size="small"
            placeholder="用户搜索"
            clearable
            @change="serchPutChange"
          ></el-input>
          <el-button type="warning" icon="el-icon-search" size="small" @click.native.prevent="btnSearch" circle style="margin:0px"></el-button>
        </div>
      <hr />
    </div>
    <div class="mgmain">
      <el-table
        ref="multipleTable"
        :data="tableData"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" label="ID"></el-table-column>
        <el-table-column label="用户" prop="username" v-slot="newUsername">
          <template>
              <router-link :to="{name:'datamg',query:{id:newUsername.row.id}}"  class='newUserStyle' tag="div" >{{newUsername.row.username}}</router-link>
          </template>
        </el-table-column>
        <el-table-column label="数量" prop="num"></el-table-column>
        <el-table-column label="模式" prop="mode">
          <template v-slot="newmode">
            <div>{{newmode.row.mode|filterMode}}</div>
          </template>
        </el-table-column>
        <el-table-column label="权限" prop="isSuperUser">
          <template v-slot="SuperUser">
            <div>{{SuperUser.row.isSuperUser|filterSuperUser}}</div>
          </template>
        </el-table-column>

        <el-table-column label="目标" prop="target" width="200px"></el-table-column>
        <el-table-column align="right" label="地址">
          <template slot="header">
            <span class="spstyle">编辑</span>
          </template>
          <template v-slot="scope">
            <el-button size="mini" @click.native.prevent="handleEdit(scope.$index, scope.row)">Edit</el-button>
            <el-button
              size="mini"
              type="danger"
              @click.native.prevent="handleDelete(scope.$index, scope.row)"
            >Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- Form -->
      <el-dialog
        :title="title==='NEW'?'添加用户':'编辑用户'"
        :visible.sync="dialogFormVisible"
        :width="isnewWidth"
        class="resetWidth"
        :before-close="handleClose"
      >
        <el-form :model="form" :rules="rules" ref="ruleForm">
          <el-form-item label="用户" :label-width="formLabelWidth" prop="username">
            <el-input v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="isBoolShow" label="密码" :label-width="formLabelWidth" prop="password">
            <el-input v-model="form.password" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="数量" :label-width="formLabelWidth" prop="num">
            <el-input v-model="form.num" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="目标" :label-width="formLabelWidth" prop="target">
            <el-input v-model="form.target" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="模式" :label-width="formLabelWidth" prop="mode">
            <el-checkbox-group v-model="form.mode" :max="1">
              <el-checkbox label="1">1.DNS多对一</el-checkbox>
              <el-checkbox label="2">2.DNS多对多</el-checkbox>
              <el-checkbox label="5">5.SQL多对一</el-checkbox>
              <el-checkbox label="6">6.SQL多对多</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="高级" :label-width="formLabelWidth">
            <el-checkbox-group v-model="form.isSuperUser" :max="1" @change="openBtn">
              <el-checkbox label="1">密码是否启用</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="cancel">取 消</el-button>
          <el-button type="primary" @click.native.prevent="confirm">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div class="mgfooter">
      <div class="btnStyle">
        <el-button type="primary" icon="el-icon-share" @click.native.prevent="selectAllData">全选</el-button>
        <el-button type="primary" icon="el-icon-delete" class="btnDelStyle" @click.native.prevent="delAllData">全删</el-button>
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
import { DeepClone } from "@/utils/newmg.js";
const defaultForm = {
  username: "",
  password: "",
  num: "",
  target: "",
  mode: [],
  isSuperUser: []
};

const defaultPagin = {
  currentPage: 1,
  pagesizes: [10, 20, 50],
  pagesize: 10,
  total: 10
};

const defaultTableData = [];

const usernameVali = [
  { required: true, message: "请输入用户名称", trigger: "blur" },
  { min: 5, max: 128, message: "长度在 5 到 128 个字符", trigger: "blur" }
];
const passwordVali = [
  { required: true, message: "请输入密码", trigger: "blur" },
  { min: 5, max: 128, message: "长度在 5 到 128 个字符", trigger: "blur" }
];
const targetVali = [
  { required: true, message: "请输入目标地址", trigger: "blur" },
  { min: 1, message: "最少1个字符", trigger: "blur" }
];

export default {
  data() {
    const numVali = (rule, value, callback) => {
      const valueStr = value.toString();
      if (valueStr.trim() === "") {
        return callback(new Error("请输入数量"));
      }
      const objRegExp = /^[0-9]+$/;
      const temp = objRegExp.test(valueStr);
      if (temp) {
        return callback();
      } else {
        return callback(new Error("只能输入数字，不能有空格与字母等"));
      }
    };
    const modeVali = (rule, value, callback) => {
      if (value.length === 1) {
        return callback();
      } else {
        return callback(new Error("请选择模式"));
      }
    };
    return {
      // 规则
      rules: {
        username: usernameVali,
        num: [{ validator: numVali, trigger: "blur", required: true }],
        password: passwordVali,
        target: targetVali,
        mode: [{ validator: modeVali, required: true }]
      },
      search: "",
      title: "NEW",
      isBoolShow: false,
      isnewWidth: "430px",
      newScreen: document.documentElement.clientWidth,
      tableData: Object.assign([], defaultTableData),
      search: "",
      dialogFormVisible: false,
      pagin: Object.assign({}, defaultPagin),
      form: Object.assign({}, defaultForm),
      formLabelWidth: "55px",
      radio: "1",
      checkList: []
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
            .dispatch("usermg/delUserData", JSON.stringify(newD))
            .then(response => {
              this.pagin.total -= 1;
              this.getAllUsers();
            });
        }
      } else {
        return false;
      }
    },
    // 编辑用户
    handleEdit(index, row) {
      this.title = "EDIT";
      this.dialogFormVisible = true;
      if (row["isSuperUser"]) {
        this.isBoolShow = true;
      }
      this.form = {
        username: row["username"],
        password: "",
        num: row["num"],
        target: row["target"],
        mode: row["mode"] ? eval(row["mode"]) : [],
        isSuperUser: row["isSuperUser"] ? ["1"] : []
      };
    },
    // 删除用户
    handleDelete(index, row) {
      let newD = new Array();
      newD.push({ id: row.id });
      this.$store
        .dispatch("usermg/delUserData", JSON.stringify(newD))
        .then(response => {
          // console.log(response);
          this.pagin.total -= 1;
          this.getAllUsers();
        });
    },
    handleSelectionChange(val) {
      // console.log(val)
      this.multipleSelection = val;
    },
    // 当前显示的页数
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      let isR = val * this.pagin.currentPage > this.pagin.total;
      if (isR) {
        this.pagin.pagesize = val;
        this.handleCurrentChange(1);
        return false;
      }
      this.pagin.pagesize = val;
      this.getAllUsers();
    },
    // 当前页码
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.pagin.currentPage = val;
      this.getAllUsers();
    },
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.form = Object.assign({}, defaultForm);
      this.openBtn();
      this.$refs["ruleForm"].resetFields();
      done();
    },
    // 提交对话框表单
    confirm() {
      this.$refs["ruleForm"].validate(vali => {
        if (!vali) {
          return false;
        } else {
          this.dialogFormVisible = false;
          const newArr = new FormData();
          const newStr = JSON.stringify(this.form);
          newArr.append("data", newStr);
          this.$store.dispatch("usermg/addUserData", newArr).then(response => {
            this.getAllUsers();
          });
          this.form = Object.assign({}, defaultForm);
          this.openBtn();
          this.$refs["ruleForm"].resetFields();
        }
      });
    },
    // 取消对话框
    cancel() {
      this.dialogFormVisible = false;
      this.form = Object.assign({}, defaultForm);
      this.openBtn();
      this.$refs["ruleForm"].resetFields();
    },
    // 是否启用密码
    openBtn() {
      if (this.form.isSuperUser.length) {
        this.isBoolShow = true;
      } else {
        this.isBoolShow = false;
      }
    },
    // 获取用户所有数据
    getAllUsers() {
      if (
        (this.pagin.currentPage - 1) * this.pagin.pagesize ==
          this.pagin.total &&
        this.pagin.currentPage - 1 > 0
      ) {
        this.pagin.currentPage -= 1;
      }
      let newObj = {
        currentpage: this.pagin.currentPage === null ? 1 : this.pagin.currentPage,
        pagesize: this.pagin.pagesize,
        search:this.search
      };
      this.$store.dispatch("usermg/getUserData", newObj).then(response => {
        this.tableData = response.data;
        this.pagin.total = response.total;
      });
    },
    // 按下搜索时触发
    btnSearch() {
      if(this.search.trim()===""){
        return false
      }
      this.getAllUsers();
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
      let newVal = val.toString().trim();
      if (newVal == "") {
        this.getAllUsers();
      }
    }
  },
  // 对话框宽度设置
  mounted() {
    if (document.body.offsetWidth < 500) {
      this.isnewWidth = null;
    }
    window.changeWithValueA = this._data;
    // 监听屏幕宽度变化用于window事件
    window.onresize = function() {
      this.changeWithValueA.newScreen = document.body.offsetWidth;
      this.newScreen = document.body.offsetWidth;
    };
  },
  created() {
    this.getAllUsers();
  },
  filters: {
    filterMode: function(data) {
      const newObj1 = {
        "1": "1.DNS多对一",
        "2": "2.DNS多对多",
        "5": "5.SQL多对一",
        "6": "6.SQL多对多"
      };
      return newObj1[eval(data)];
    },
    filterSuperUser: function(data) {
      if (data) {
        return "VIP";
      }
      return "普通";
    }
  },
  // 监听屏幕宽度变化用于VUE事件
  watch: {
    newScreen: function(val) {
      if (val < 500) {
        this.isnewWidth = null;
      } else {
        this.isnewWidth = "430px";
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    window.onresize = null;
    this.$store.commit("usermg/SET_ROUTE_ID",to.query.id)
    next();
  }
};
</script>

<style scoped>
.mgheader button {
  margin: 10px 0px 0px 30px;
}
.mgmain {
  margin-left: 22px;
}

.spstyle {
  margin-right: 61px;
}

.mgheader hr {
  border-bottom: 1px solid #304156(3, 78, 252);
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

.newWidth {
  width: 430px;
}
.btnDelStyle {
  background-color: #f56c6c;
  border-color: #f56c6c;
}
.newUserStyle:hover {
  color: blue;
  font-size: 16px;
  cursor:pointer;
}

.searchStyle {
  width: 200px;
  margin-left: 20px;
}

.msgsearch {
  display: inline-block;
}
</style>