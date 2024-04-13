<template>
  <div class="app">
    <div class='title'>
      <div class="name">Image<p>Captioning</p>
      </div>
      <ul class="button">
        <li class="icon">
          <a  href="#">
            <div class="iconfont icon-shujutansuo"></div>
            <span>探索</span>
          </a>
          <div class="dropdown">
            <a href="#">其他用户</a>
            <a href="#">数据库</a>
          </div>
        </li>

        <li class="icon">
          <a href="#" >
          <div class="iconfont icon-denglu"> </div>
          <span>登录</span>
        </a>
          <div class="dropdown">
            <a href="#">登录</a>
            <a href="#">注册</a>
          </div>
        </li>
        <li class="icon">
          <a href="#" >
          <div class="iconfont icon-suiji"></div>
          <span>随机</span>
        </a>
        </li>
        
      </ul>
    </div> 
    <!--正文层-->
    <!-- 导航区 -->
    <div class="navigate">
      <RouterLink replace :to="{ path: '/home' }" active-class="active"><span>首页</span></RouterLink>
      <RouterLink replace :to="{ path: '/upcaption' }" active-class="active">图像描述</RouterLink>
      <RouterLink replace :to="{ path: '/databases' }" active-class="active">数据库</RouterLink>
      <RouterLink replace :to="{ path: '/about' }" active-class="active">关于</RouterLink>
    </div>
    <!-- 展示区 -->
    <div class="bock">
      <div class="main-content">
        <RouterView></RouterView>
      </div>
    </div>

  </div>
</template>

<script lang='ts' setup name="image captioning">

import { RouterView, RouterLink } from 'vue-router'

</script>

<style scoped>
@import url('./assets/css/app.css');
</style>