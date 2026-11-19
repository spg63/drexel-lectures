<script setup lang="ts">
defineProps<{ kicker?: string }>()
</script>

<template>
  <div class="slidev-layout cover">
    <div class="ring ring-a" />
    <div class="ring ring-b" />
    <div class="dot" />
    <div class="cover-body">
      <div v-if="kicker" class="kicker">{{ kicker }}</div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.cover {
  background: var(--dx-blue);
  color: var(--on-dark);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 0 4rem;
}
.cover-body { position: relative; z-index: 1; max-width: 70%; }
.kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--dx-gold);
  margin-bottom: 1.1rem;
}
.cover :deep(h1) {
  color: #fff;
  font-size: 3.6rem;
  margin-bottom: 0.9rem;
  padding-bottom: 0;
}
.cover :deep(h1::after) { display: none; }
.cover :deep(p) { font-size: 1.35rem; color: #d9dfe8; margin: 0.2rem 0; }
.cover :deep(small) { display: block; margin-top: 2.2rem; font-size: 0.75rem; color: var(--on-dark-muted); max-width: 34rem; line-height: 1.4; }
.ring { position: absolute; border-radius: 50%; border: 3px solid var(--dx-gold); }
.ring-a { width: 26rem; height: 26rem; right: -8rem; bottom: -11rem; opacity: 0.9; }
.ring-b { width: 15rem; height: 15rem; right: 6rem; bottom: -9rem; border-color: rgba(255, 255, 255, 0.18); }
.dot { position: absolute; width: 1.1rem; height: 1.1rem; border-radius: 50%; background: var(--dx-gold); right: 15rem; top: 6rem; }
</style>
