<script setup lang="ts">
// <Aside>Remember: delete from the tail!</Aside>
// <Aside label="Exam tip">...</Aside>
defineProps<{ label?: string }>()
</script>

<template>
  <div class="aside">
    <span v-if="label" class="aside-label">{{ label }}</span>
    <slot />
  </div>
</template>
