<script setup lang="ts">
// Picture-first slide: title, one big figure filling the rest, optional caption.
// frontmatter: caption
defineProps<{ caption?: string }>()
</script>

<template>
  <div class="slidev-layout figure">
    <slot />
    <div v-if="caption" class="caption figure-caption">{{ caption }}</div>
    <div class="dx-pgnum">{{ $page }}</div>
  </div>
</template>

<style scoped>
/* grid gives the figure row a definite height, so the image can scale to fit it */
.figure { display: grid; grid-template-rows: auto minmax(0, 1fr) auto; }
.figure :deep(> p), .figure :deep(> .figs) { min-height: 0; height: 100%; margin: 0; display: flex; justify-content: center; align-items: center; }
.figure :deep(img) { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; mix-blend-mode: multiply; }
.figure :deep(> img) { justify-self: center; align-self: center; min-height: 0; }
.figure-caption { margin-top: 0.5rem; }
</style>
