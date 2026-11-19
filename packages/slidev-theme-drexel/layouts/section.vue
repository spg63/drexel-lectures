<script setup lang="ts">
// Section divider. frontmatter: kicker (small gold label above the title)
defineProps<{ kicker?: string }>()
</script>

<template>
  <div class="slidev-layout section">
    <div class="bar" />
    <div class="body">
      <div v-if="kicker" class="kicker">{{ kicker }}</div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.section { background: var(--dx-blue); color: var(--on-dark); display: flex; align-items: center; padding: 0 4rem; position: relative; overflow: hidden; }
.bar { position: absolute; left: 0; top: 0; bottom: 0; width: 0.55rem; background: var(--dx-gold); }
.body { max-width: 78%; }
.kicker { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--dx-gold); margin-bottom: 0.9rem; }
.section :deep(h1) { color: #fff; font-size: 3rem; padding-bottom: 0; margin-bottom: 0.7rem; }
.section :deep(h1::after) { display: none; }
.section :deep(p) { font-size: 1.25rem; color: var(--on-dark-muted); margin: 0.2rem 0; }
</style>
