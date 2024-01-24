<template>
  <div class="app">
    <div class='title'><h1>image captioning</h1></div> <!--正文层-->
    <!-- 导航区 -->
    <div class="navigate"> 
 <RouterLink replace :to="{path:'/home'}" active-class="active"><span>首页</span></RouterLink>    
 <RouterLink replace :to="{path:'/databases'}" active-class="active">数据库</RouterLink>    
 <RouterLink replace :to="{path:'/about'}" active-class="active">关于</RouterLink>    
    </div>
    <!-- 展示区 -->
    <div class="main-content">
      <RouterView></RouterView>
        </div>
  </div>
</template>

<script lang='ts' setup name="image captioning" >

  import {RouterView,RouterLink} from 'vue-router'

</script>

<style scoped>

.app {
 
    width:100%;
    height: 100%;
    position: fixed;
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    background-position: center;
    
    background-color: rgba(119, 215, 226, 0.318);
    margin: 0;
}
  .title{
  background-color: rgba(106, 108, 235, 0.553);
  height: 15%; 
  width: 100%;
  text-align: center;
}
.main-content {
    flex-grow: 1;
    margin: 0;
    backdrop-filter:unset;
    background-color: rgba(223, 223, 234, 0.8);
  }

  .navigate{
  margin: 0;
  height: 85%;
  width: 10%;
  border: 1px solid;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(0, 255, 255, 0.319);
  }
  .navigate a{
    margin: 0;
    width: 100%;
    height: 10%;
  }
  a {
  color: #0faaec;
  text-decoration: none;
  display:flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  position: relative;
}
a::after {
  content: '';
  width: 80%; 
  display: block; /* 设置伪类为块级元素，这样可以设置宽度 */
  border-bottom: 2px solid black; 
  position: absolute; 
  bottom: 0; 
}
  a.active {
    background-color: rgba(14, 129, 230, 0.685);
    
  }

</style>