// Generated GraphQL types, do not edit manually.

import * as Types from '../../graphql/types';

export type StartSensorMutationVariables = Types.Exact<{
  sensorSelector: Types.SensorSelector;
}>;

export type StartSensorMutation = {
  __typename: 'DagitMutation';
  startSensor:
    | {
        __typename: 'PythonError';
        message: string;
        stack: Array<string>;
        errorChain: Array<{
          __typename: 'ErrorChainLink';
          isExplicitLink: boolean;
          error: {__typename: 'PythonError'; message: string; stack: Array<string>};
        }>;
      }
    | {
        __typename: 'Sensor';
        id: string;
        sensorState: {__typename: 'InstigationState'; id: string; status: Types.InstigationStatus};
      }
    | {__typename: 'SensorNotFoundError'}
    | {__typename: 'UnauthorizedError'};
};

export type StopRunningSensorMutationVariables = Types.Exact<{
  jobOriginId: Types.Scalars['String'];
  jobSelectorId: Types.Scalars['String'];
}>;

export type StopRunningSensorMutation = {
  __typename: 'DagitMutation';
  stopSensor:
    | {
        __typename: 'PythonError';
        message: string;
        stack: Array<string>;
        errorChain: Array<{
          __typename: 'ErrorChainLink';
          isExplicitLink: boolean;
          error: {__typename: 'PythonError'; message: string; stack: Array<string>};
        }>;
      }
    | {
        __typename: 'StopSensorMutationResult';
        instigationState: {
          __typename: 'InstigationState';
          id: string;
          status: Types.InstigationStatus;
        } | null;
      }
    | {__typename: 'UnauthorizedError'};
};
