import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import {Transition} from 'react-transition-group';

export default class Modal extends React.Component {
  render() {
    const {show, onHide, title, children, size} = this.props;

    let ignoringNext = false;
    const ignoreNext = () => ignoringNext = true;
    const modalClicked = () => {
      if (ignoringNext) {
        ignoringNext = false;
        return;
      }
      onHide();
    };

    return <Transition in={show} timeout={300} enter={false}>
      {state =>
        <div>
          <div
            className={classNames('modal', 'fade', {in: state === 'entered'})}
            style={{display: ['entered', 'exiting'].includes(state) ? 'block' : 'none'}}
            onClick={modalClicked}
          >
            <div
              className={classNames('modal-dialog', size && `modal-${size}`)} role="document" onMouseDown={ignoreNext}
            >
              <div className="modal-content">
                <div className="modal-header">
                  <button
                    type="button" className="close" aria-label="Fermer"
                    onClick={onHide}
                  >
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <h4 className="modal-title">{title}</h4>
                </div>
                {children}
              </div>
            </div>
          </div>
          {['entered', 'exiting'].includes(state) &&
            <div className={classNames('modal-backdrop', 'fade', state === 'entered' && 'in')} onClick={onHide}/>
          }
        </div>
      }
    </Transition>;
  }
}

Modal.propTypes = {
  children: PropTypes.node,
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func,
  size: PropTypes.string,
};

Modal.defaultProps = {
  onHide: () => {
  }
};

Modal.Body = ({children}) => <div className="modal-body">
  {children}
</div>;
Modal.Body.displayName = 'Modal.Body';
Modal.Body.propTypes = {children: PropTypes.node};

Modal.Footer = ({children}) => <div className="modal-footer">
  {children}
</div>;
Modal.Footer.displayName = 'Modal.Footer'
Modal.Footer.propTypes = {children: PropTypes.node};