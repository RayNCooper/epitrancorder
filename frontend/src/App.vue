<script setup lang="ts">
import { ref, onMounted } from 'vue'

type Language = {
  id: number, iso: string, label: string
}

const languages = ref<Language[]>([])
const selectedLang = ref<Language | null>(null)
const text = ref("")
const loading = ref(false)
const ipaText = ref("")
const xsampaText = ref("")

const errorMessage = ref("")
const displayError = ref(false)

onMounted(async () => {
  const langData: Language[] = await (await fetch("http://127.0.0.1:8000/languages")).json()
  languages.value.push(...langData)
})

const transliterateText = () => {
  if (selectedLang.value) {
    loading.value = true
    const requestBody = {
      "native_text": text.value
    }

    ipaText.value = ""
    xsampaText.value = ""

    const ipaTransliteration = fetch(`http://127.0.0.1:8000/transliterate/${selectedLang.value.id}?transliteration_type=IPA`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: JSON.stringify(requestBody)
    })

    const xsampaTransliteration = fetch(`http://127.0.0.1:8000/transliterate/${selectedLang.value.id}?transliteration_type=X-SAMPA`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
        'accept': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
    const response = Promise.all([ipaTransliteration, xsampaTransliteration])

    response.then(async (res) => {
      res.forEach(async (r) => {
        /* For Simplicity's sake, I will have the JSON be parsed via await - Again, yes I know this might lead to problems if the main (read: the only thread) thread is blocked for too long */
        if (r.url.includes("IPA")) ipaText.value = await r.json()
        else if (r.url.includes("X-SAMPA")) xsampaText.value = await r.json()
      })
      loading.value = false
    }, (err) => {
      console.log(err)
      loading.value = false
    })
  } else {
    errorMessage.value = "Select a Language!"
    displayError.value = true
    setTimeout(() => {
      errorMessage.value = ""
      displayError.value = false
    }, 3000);
  }
}
</script>

<template>
  <div class="container">
    <h1 style="margin: auto; margin-bottom: 4px;">Epitrancorder</h1>
    <span style="margin: auto">
      (
      <a href="https://pypi.org/project/epitran/">epitran</a> +
      <a href="https://en.wikipedia.org/wiki/Tricorder">tricorder</a> )
    </span>
    <h2>1. Select a Language:</h2>
    <select v-model="selectedLang">
      <option v-for="lang in languages" :value="lang" :key="lang.id">{{ lang.label }}</option>
    </select>
    <h2>2. Input your Text:</h2>
    <textarea cols="30" rows="10" v-model="text"></textarea>

    <h2>3. Transliterate</h2>
    <button style="font-weight: bolder" @click="transliterateText">Transliterate</button>

    <h3 style="color:blue" class="logMessage" v-if="loading">Loading...</h3>
    <h3 style="color:red" class="logMessage" v-if="displayError">{{ errorMessage }}</h3>
    <div class="split">
      <div>
        <span class="transliterationSpan">X-SAMPA</span>
        <p>{{ xsampaText }}</p>
      </div>
      <div>
        <span class="transliterationSpan">IPA</span>
        <p>{{ ipaText }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
.container,
textarea {
  font-family: "Roboto", sans-serif;
}

.container {
  display: flex;
  justify-content: center;
  flex-direction: column;
  margin: 2em;
  padding: 1em;
}
.split {
  margin-top: 1em;
  display: flex;
  flex-direction: row;
}
.split > div,
button,
select {
  width: 100%;
  text-align: center;
  padding: 1em;
}

.logMessage {
  position: absolute;
  bottom: 1em;
  left: 50%;
  transform: translate(-50%, -50%);
}

.transliterationSpan {
  font-size: large;
  font-weight: bold;
}

a {
  color: blue;
}
</style>
