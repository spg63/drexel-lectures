<script setup lang="ts">
// Title across the top, text and figure side by side.
// frontmatter: flip (figure on the left), ratio (CSS grid columns)
const props = withDefaults(defineProps<{ flip?: boolean; ratio?: string }>(), { flip: false, ratio: '1.1fr 1fr' })
</script>

<template>
  <div class="slidev-layout split">
    <div class="split-head"><slot /></div>
    <div class="split-body" :style="{ gridTemplateColumns: props.ratio }" :class="{ flip: props.flip }">
      <div class="split-text"><slot name="left" /></div>
      <div class="split-fig"><slot name="right" /></div>
    </div>
    <div class="dx-pgnum">{{ $page }}</div>
  </div>
</template>

<style scoped>
.split { display: flex; flex-direction: column; }
.split-body { display: grid; gap: 2rem; flex: 1; min-height: 0; }
.split-body.flip .split-text { order: 2; }
.split-fig { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 0; }
.split-fig :deep(img) { max-height: 100%; max-width: 100%; object-fit: contain; }
</style>
