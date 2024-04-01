<template>
  <div>
<h1>Databases</h1>
<div class="navigate">
  <RouterLink replace :to="{name:'图片'}" active-class="active">图片</RouterLink>    
  <RouterLink replace :to="{name:'描述'}" active-class="active">描述</RouterLink> 
</div>
   
  </div>
  <!-- 展示区 -->
  <div class="data-content">
      <RouterView></RouterView>
        </div>
</template>

<script lang='ts' setup>

</script>

<style scoped>
.navigate{
  height: 50px;
  display: flex;
}
.data-content {
  background-color:rgba(115, 223, 250, 0.337);
  margin: 0 auto;
  margin-top: 60px;
  border-radius: 10px;
  width: 90%;
  height: 60%;
  border: 1px solid;
}
a {
  color: #22129b;
  width: 10%;
  height: 100%;
  margin-right: 20px;
  display:flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  border: 3px solid;
  border-color: rgba(127, 255, 212, 0.749);
  border-radius: 10px;
  font-size: 25px;
}
.active {
    background-color: rgba(248, 252, 2, 0.759);
  }
</style>