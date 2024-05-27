<template>
  <div class="login-modal">
    <div class="login-from">
      <el-form :model="form" ref="formRef" :rules="rules" label-width="auto" style="max-width: 600px">
        <el-form-item label="用户名" prop="regusername">
          <el-input v-model="form.regusername" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.regpassword" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirmPassword" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit">注册</el-button>
          <el-button>清空</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang='ts' setup>
import { reactive, ref } from 'vue'
import type { FormRules } from 'element-plus'
import {ElMessage} from 'element-plus'
const formRef = ref()
const form = reactive({
  regusername: '',
  regpassword: '',
  confirmPassword: '',
  loginUsername: '',
  loginPassword: '',
})

const rules = reactive<FormRules>({
  regusername: [
    { required: true, message: "用户名不能为空" ,trigger:'blur'},
    // {pattern:'',message:'用户名不能使用特殊字符'}
  ]
})

function onSubmit() {
formRef.value?.validate().catch(()=>{
  ElMessage.error("注册信息不符合规范")
  return 
})

}

</script>

<style scoped>
@import url('../../assets/css/login.css')
</style>