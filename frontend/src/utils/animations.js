import { gsap } from 'gsap'

// 卡片进入动画
export function cardEnterAnimation(el, done) {
  gsap.from(el, {
    opacity: 0,
    y: 20,
    duration: 0.3,
    onComplete: done
  })
}

// 卡片离开动画
export function cardLeaveAnimation(el, done) {
  gsap.to(el, {
    opacity: 0,
    y: -20,
    duration: 0.3,
    onComplete: done
  })
}

// 列表项动画
export function listItemAnimation(el, done) {
  gsap.from(el, {
    opacity: 0,
    x: -20,
    duration: 0.3,
    onComplete: done
  })
}

// 页面切换动画
export function pageTransition(el, done) {
  gsap.from(el, {
    opacity: 0,
    scale: 0.95,
    duration: 0.3,
    onComplete: done
  })
}

// 弹出动画
export function popAnimation(el, done) {
  gsap.from(el, {
    scale: 0.6,
    opacity: 0,
    duration: 0.3,
    ease: 'back.out(1.7)',
    onComplete: done
  })
}

// 抖动动画
export function shakeAnimation(el) {
  gsap.to(el, {
    x: [-5, 5, -5, 5, 0],
    duration: 0.5,
    ease: 'power2.inOut'
  })
}

// 脉冲动画
export function pulseAnimation(el) {
  gsap.to(el, {
    scale: 1.05,
    duration: 0.3,
    repeat: 1,
    yoyo: true,
    ease: 'power2.inOut'
  })
}

// 滑动菜单动画
export function slideMenuAnimation(el, done, direction = 'right') {
  const x = direction === 'right' ? 100 : -100
  
  gsap.from(el, {
    x: `${x}%`,
    opacity: 0,
    duration: 0.3,
    ease: 'power2.out',
    onComplete: done
  })
}

// 加载动画
export function loadingAnimation(el) {
  gsap.to(el, {
    rotation: 360,
    duration: 1,
    repeat: -1,
    ease: 'none'
  })
}

// 数值变化动画
export function numberAnimation(el, startValue, endValue, prefix = '', suffix = '') {
  gsap.to(el, {
    innerText: endValue,
    duration: 1,
    snap: { innerText: 1 },
    onUpdate: () => {
      el.innerText = prefix + el.innerText + suffix
    }
  })
} 