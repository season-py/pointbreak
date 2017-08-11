import { Component, ViewChild } from '@angular/core';

import { AlertController, App, FabContainer, List, ModalController, NavController, ToastController, LoadingController } from 'ionic-angular';

/*
  To learn how to use third party libs in an
  Ionic app check out our docs here: http://ionicframework.com/docs/v2/resources/third-party-libs/
*/
// import moment from 'moment';

import { CoinData } from '../../providers/coin-data';
import { ConferenceData } from '../../providers/conference-data';
import { UserData } from '../../providers/user-data';



@Component({
  selector: 'page-coin',
  templateUrl: 'coin.html'
})
export class CoinPage {

  @ViewChild('coinList', { read: List }) coinList: List;
  coins: any = []

  constructor(
    public alertCtrl: AlertController,
    public app: App,
    public loadingCtrl: LoadingController,
    public modalCtrl: ModalController,
    public navCtrl: NavController,
    public toastCtrl: ToastController,
    public confData: ConferenceData,
    public coinData: CoinData,
    public user: UserData,
  ) {}

  ionViewDidLoad() {
    this.app.setTitle('Coins');
    this.updateCoin();
  }

  updateCoin() {
    // Close any open sliding items when the schedule updates
    this.coinList && this.coinList.closeSlidingItems();

    this.coinData.load().subscribe((data: any) => {
      this.coins = data.coins;
    });
  }

  presentFilter() {
  }

  goToSessionDetail() {
  }

  addFavorite() {
  }

  removeFavorite() {
  }

  openSocial(network: string, fab: FabContainer) {
    let loading = this.loadingCtrl.create({
      content: `Posting to ${network}`,
      duration: (Math.random() * 1000) + 500
    });
    loading.onWillDismiss(() => {
      fab.close();
    });
    loading.present();
  }

  doRefresh() {
  }
}
