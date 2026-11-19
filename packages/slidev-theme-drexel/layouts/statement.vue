<script setup lang="ts">
// One idea, big: a discussion prompt, a definition, a punchline.
// frontmatter: kicker (small label above, e.g. "Discuss" or "Quick check")
defineProps<{ kicker?: string }>()
</script>

<template>
  <div class="slidev-layout statement">
    <div class="inner">
      <div v-if="kicker" class="kicker">{{ kicker }}</div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.statement { display: flex; align-items: center; justify-content: center; text-align: center; }
.inner { max-width: 80%; }
.kicker { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--dx-blue); background: var(--dx-gold); padding: 0.15rem 0.6rem; border-radius: 99px; margin-bottom: 1.1rem; }
.statement :deep(h1) { font-size: 2.6rem; line-height: 1.15; padding-bottom: 0; margin-bottom: 0.8rem; text-wrap: balance; }
.statement :deep(h1::after) { display: none; }
.statement :deep(p) { font-size: 1.3rem; color: var(--muted); }
</style>
