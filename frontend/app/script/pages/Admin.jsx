import React, { Component, Fragment } from 'react';
import API from '../api';
import utils from '../utils';
import socketIOClient from 'socket.io-client';
import 'react-notifications/lib/notifications.css';
import { NotificationContainer, NotificationManager } from 'react-notifications';
import './Admin.scss';
import DefaultHeader from "Parts/DefaultHeader";

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = {
      detectionList: [],
      currentTime: null,
      notificationPolicy: {},
      notificationEnabled: false,
      notificationNumThreshold: 10,
    };
    this.socket = null;
  }

  componentDidMount() {
    this.setCurrentTime();
    this.setSocketio();
    this.setLatestDetection();
  }

  handleInputChange = (evt) => {
    this.setState({[evt.target.name]: evt.target.value})
  }

  setCurrentTime() {
    setInterval(() => {
      this.setState({
        currentTime: utils.formatDateForDebug(new Date()),
      });
    }, 1000);
  }

  setSocketio() {
    this.socket = socketIOClient("/");
    // this.socket = socketIOClient("/", {transports: ['polling']});
    // this.socket = socketIOClient(endpoint, {transports: ['websocket']})
    this.socket.on('detection', data => {
      console.log('socketio data:' + JSON.stringify(data));
      this.updateDetection(data);
      switch (data.event) {
        case 'check_in':
          NotificationManager.success(`memberId=${data.memberId} name=${data.username} ${data.event}`);
          break;
        case 'check_out':
          NotificationManager.success(`memberId=${data.memberId} name=${data.username} ${data.event}`);
          break;
        case 'warning':
          NotificationManager.warning(data.msg, 'warning', 6000);
          break;
        default:
          // only show message for the first event.
          NotificationManager.info(`${JSON.stringify(data)}`, 6000);
      }
      // the following are for debug purpose.
      this.socket.on('ping', () => {
        console.log('ping');
      });
      this.socket.on('pong', latency => {
        console.log('latency is ' + latency);
      });
    });
  }

  // renderConfirm() {
  //     return (
  //     <Confirm
  //     onConfirm={this.onConfirm}
  //     body="Are you sure you want to delete this?"
  //     confirmText="Confirm Delete"
  //     title="Deleting Stuff">
  //     <button>Delete Stuff</button>
  //     </Confirm>
  //     )
  // }

  // onConfirm = () => {
  //     console.log("confirmed");
  // }

  forceCheckOut = item => {
    console.log('force checkout: ' + JSON.stringify(item));
    const event = {
      cameraId: 'camera2',
      camera_data: {
        header_count: 1,
        profiles: [
          {
            userId: item.userId,
          },
        ],
      },
    };
    API.accessors.detections.create(event)
      .then(res => {
        console.log(res);
      })
      .catch(error => {
        console.log(error);
      });
  };

  setLatestDetection() {
    API.accessors.detections.list()
      .then(res => {
        console.log(res);
        this.setState({
          detectionList: res.data,
        });
      })
      .catch(error => {
        console.log(error);
      });
  }

  setNotificationPolicy = (evt) => {
    evt.preventDefault();
    const policy = {
      "notificationEnabled": this.state.notificationEnabled == "true",
      "notificationNumThreshold": parseInt(this.state.notificationNumThreshold),
    }
    console.log(policy)
    API.accessors.policies.update('notification', policy)
      .then(res => {
        console.log(res);
        this.setState({
          notificationPolicy: res.data,
        });
      })
      .catch(error => {
        console.log(error);
      });
  }

  getNotificationPolicy = () => {
    API.accessors.policies.get("notification")
      .then(res => {
        console.log(res);
        this.setState({
          notificationPolicy: res.data,
        });
      })
      .catch(error => {
        console.log(error);
      });
  }

  updateDetection(detection) {
    if (!detection) {
      return;
    }
    let detectionList = [];
    detectionList.push(detection);
    for (const io of this.state.detectionList) {
        detectionList.push(io);
    }
    console.log('new list is:');
    console.log(detectionList);

    this.setState({
      detectionList: detectionList,
    });
  }

  render() {
    return (
      <div className='container'>
        <NotificationContainer />
        <DefaultHeader />
        <h1>Admin Debug page</h1>
        <div>time: {this.state.currentTime}</div>
        <div>
          <h3>notification policy</h3>
          <button onClick={this.getNotificationPolicy}>get current policy</button>
          <div>
            {JSON.stringify(this.state.notificationPolicy)}
          </div>
          <form>
              notificationEnabled: <input type='text' name='notificationEnabled' value={this.state.notificationEnabled} onChange={this.handleInputChange} />
              notificationNumThreshold: <input type='text' name='notificationNumThreshold' value={this.state.notificationNumThreshold} onChange={this.handleInputChange} />
              <button onClick={this.setNotificationPolicy}>change policy</button>
          </form>
        </div>
        <div>
          <h3>live stream</h3>
          <table className='table'>
            <thead>
              <tr>
                <th scope='col'>#</th>
                <th scope='col'>cameraId</th>
                <th scope='col'>status</th>
                <th scope='col'>image</th>
                <th scope='col'>persons</th>
                <th scope='col'>timestamp</th>
                <th scope='col'>formatted timestamp</th>
                <th scope='col'>createdAt</th>
              </tr>
            </thead>
            <tbody>
              {this.state.detectionList.map((item, idx) => {
                return (
                  <Fragment key={idx}>
                    <tr>
                      <th scope='row'>{idx}</th>
                      <td> {item.cameraId} </td>
                      <td> {item.status} </td>
                      <td> {JSON.stringify(item.image)} </td>
                      <td> {JSON.stringify(item.persons)} </td>
                      <td> {item.timestamp} </td>
                      <td> {utils.formatDateForDebug(new Date(item.timestamp))} </td>
                      <td> {item.createdAt} </td>
                      {/* <td> <button onClick={() => {this.renderConfirm()}}>force-check-out</button> </td> */}
                    </tr>
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}
