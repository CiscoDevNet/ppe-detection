import React from 'react';
import {shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

import Index from '../../app/script/pages/index';

configure({adapter: new Adapter()});

describe('Index pages', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<Index />);
  });

  it('should exist', () => {
    expect(wrapper).toBeTruthy();
  });

  // it('should have one heading', () => {
  //   expect(wrapper.find('#heading').type()).toEqual('h2');
  // });
});
